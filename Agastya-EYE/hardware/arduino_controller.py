"""Bounded, fail-closed serial interface for the Agastya-EYE Arduino gate."""

import re
import threading
import time
import uuid
from dataclasses import replace

from .arduino_config import ArduinoConfig


COMMAND_ID_PATTERN = re.compile(r"^[0-9a-f]{32}$")
COM_PORT_PATTERN = re.compile(r"^COM[1-9]\d*$", re.IGNORECASE)
MIN_OPEN_DURATION_MS = 1000
MAX_OPEN_DURATION_MS = 30000


class HardwareError(RuntimeError):
    """Base class for optional hardware integration failures."""


class HardwareUnavailableError(HardwareError):
    """The Arduino is disabled, disconnected, or not configured."""


class HardwareProtocolError(HardwareError):
    """The Arduino did not complete the expected serial protocol."""


class ArduinoServoController:
    def __init__(self, config=None, *, serial_factory=None, sleep=time.sleep, clock=time.monotonic):
        self.config = config or ArduinoConfig.from_env()
        self._serial_factory = serial_factory
        self._sleep = sleep
        self._clock = clock
        self._lock = threading.RLock()
        self._serial = None
        self._ready = False
        self._state = "disconnected"
        self._last_error = None
        self._last_command_id = None
        self._last_command_status = None

    def is_connected(self):
        with self._lock:
            return self._serial is not None and bool(getattr(self._serial, "is_open", True))

    def is_ready(self):
        with self._lock:
            return self._ready and self._serial is not None and bool(getattr(self._serial, "is_open", True))

    def get_status(self):
        with self._lock:
            if not self.config.enabled:
                state = "disabled"
                message = "Hardware activation is disabled"
            elif self.config.configuration_error:
                state = "misconfigured"
                message = self.config.configuration_error
            elif not self.config.port:
                state = "awaiting_configuration"
                message = "Set AGASTYA_ARDUINO_PORT to the Arduino COM port"
            else:
                state = self._state
                message = self._last_error or ("Arduino is ready" if self._ready else "Arduino is disconnected")
            return {
                "enabled": self.config.enabled,
                "state": state,
                "connected": self._serial is not None and bool(getattr(self._serial, "is_open", True)),
                "ready": self._ready,
                "port": self.config.port or None,
                "baud_rate": self.config.baud_rate,
                "open_duration_ms": self.config.open_duration_ms,
                "last_error": self._last_error,
                "last_command_id": self._last_command_id,
                "last_command_status": self._last_command_status,
                "message": message,
            }

    def set_activation(self, enabled, port):
        """Set a session-only activation state and COM port without opening the port."""
        if not isinstance(enabled, bool):
            raise ValueError("Hardware enabled must be true or false")
        normalized_port = str(port or "").strip().upper()
        if enabled and not normalized_port:
            raise ValueError("Enter the Arduino COM port before enabling the gate")
        if normalized_port and not COM_PORT_PATTERN.fullmatch(normalized_port):
            if enabled:
                raise ValueError("Arduino port must use the COM number shown by Windows (for example COM5)")
            normalized_port = ""
        if enabled and self.config.configuration_error:
            raise ValueError(self.config.configuration_error)

        with self._lock:
            self._close_locked()
            self.config = replace(self.config, enabled=enabled, port=normalized_port)
            self._state = "disabled" if not enabled else "disconnected"
            self._last_error = None
            return self.get_status()

    def connect(self):
        with self._lock:
            if not self.config.enabled:
                self._ready = False
                self._state = "disabled"
                self._last_error = None
                return False
            if self.config.configuration_error:
                self._ready = False
                self._state = "misconfigured"
                self._last_error = self.config.configuration_error
                return False
            if not self.config.port:
                self._ready = False
                self._state = "awaiting_configuration"
                self._last_error = "Set AGASTYA_ARDUINO_PORT to the Arduino COM port"
                return False
            if self._ready and self._serial is not None and bool(getattr(self._serial, "is_open", True)):
                return True

            self._close_locked()
            self._state = "connecting"
            try:
                serial_factory = self._serial_factory
                if serial_factory is None:
                    import serial
                    serial_factory = serial.Serial
                self._serial = serial_factory(
                    self.config.port,
                    baudrate=self.config.baud_rate,
                    timeout=self.config.serial_timeout_seconds,
                    write_timeout=self.config.serial_timeout_seconds,
                )
                if self.config.reset_wait_seconds:
                    self._sleep(self.config.reset_wait_seconds)
                nonce = uuid.uuid4().hex
                self._write_line_locked(f"PING {nonce}")
                response = self._wait_for_line_locked(
                    lambda line: line == f"READY {nonce}" or line.startswith("ERR "),
                    self.config.handshake_timeout_seconds,
                )
                if response != f"READY {nonce}":
                    raise HardwareProtocolError("Arduino readiness handshake failed")
                self._ready = True
                self._state = "ready"
                self._last_error = None
                return True
            except Exception as error:
                self._ready = False
                self._state = "disconnected"
                self._last_error = f"{type(error).__name__}: {error}"
                self._close_locked()
                return False

    def disconnect(self):
        with self._lock:
            self._close_locked()
            self._state = "disabled" if not self.config.enabled else "disconnected"
            self._last_error = None

    def release_panel(self, command_id, duration_ms=None):
        if not COMMAND_ID_PATTERN.fullmatch(str(command_id)):
            raise ValueError("Release command ID must be a 32-character lowercase hexadecimal UUID")
        duration = self.config.open_duration_ms if duration_ms is None else duration_ms
        if isinstance(duration, bool) or not MIN_OPEN_DURATION_MS <= int(duration) <= MAX_OPEN_DURATION_MS:
            raise ValueError(f"Release duration must be between {MIN_OPEN_DURATION_MS} and {MAX_OPEN_DURATION_MS} ms")
        duration = int(duration)
        if not self.is_ready() and not self.connect():
            raise HardwareUnavailableError(self.get_status()["message"])

        with self._lock:
            if not self._ready or self._serial is None or not bool(getattr(self._serial, "is_open", True)):
                raise HardwareUnavailableError("Arduino is not ready")
            if command_id == self._last_command_id:
                raise HardwareProtocolError("Duplicate release command was blocked")
            self._last_command_id = command_id
            self._last_command_status = "sending"
            self._state = "releasing"
            try:
                self._write_line_locked(f"RELEASE {command_id} {duration}")
                acknowledgement = self._wait_for_line_locked(
                    lambda line: line in (
                        f"ACK RELEASE {command_id}",
                        f"ACK DUPLICATE {command_id}",
                    ) or line.startswith("ERR "),
                    self.config.command_timeout_seconds,
                )
                if acknowledgement != f"ACK RELEASE {command_id}":
                    raise HardwareProtocolError(
                        "Arduino rejected or did not acknowledge the release command"
                    )
                self._last_command_status = "acknowledged"
                done = self._wait_for_line_locked(
                    lambda line: line == f"DONE {command_id}" or line.startswith("ERR "),
                    duration / 1000 + self.config.command_timeout_seconds + 1,
                )
                if done != f"DONE {command_id}":
                    raise HardwareProtocolError("Arduino did not acknowledge its timed close command")
                self._last_command_status = "closed_commanded"
                self._state = "ready"
                self._last_error = None
                return {
                    "command_id": command_id,
                    "status": "closed_commanded",
                    "acknowledgement": acknowledgement,
                    "close_acknowledgement": done,
                    "duration_ms": duration,
                    "physical_position_verified": False,
                }
            except Exception as error:
                self._ready = False
                self._state = "error"
                self._last_command_status = "uncertain"
                self._last_error = f"{type(error).__name__}: {error}"
                self._close_locked()
                if isinstance(error, HardwareError):
                    raise
                raise HardwareProtocolError(self._last_error) from error

    def _write_line_locked(self, line):
        if self._serial is None:
            raise HardwareUnavailableError("Arduino serial port is not open")
        payload = (line + "\n").encode("ascii")
        written = self._serial.write(payload)
        if written != len(payload):
            raise HardwareProtocolError("Arduino serial command was only partially written")
        self._serial.flush()

    def _read_line_locked(self):
        if self._serial is None:
            raise HardwareUnavailableError("Arduino serial port is not open")
        raw = self._serial.readline()
        if not raw:
            return ""
        return raw.decode("ascii", errors="replace").strip()

    def _wait_for_line_locked(self, accepted, timeout_seconds):
        deadline = self._clock() + timeout_seconds
        while self._clock() < deadline:
            line = self._read_line_locked()
            if line and accepted(line):
                return line
        return None

    def _close_locked(self):
        serial_handle, self._serial = self._serial, None
        self._ready = False
        if serial_handle is not None:
            try:
                serial_handle.close()
            except Exception:
                pass
