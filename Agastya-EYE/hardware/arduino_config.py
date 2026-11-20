"""Environment-backed configuration for the optional Arduino servo gate."""

from dataclasses import dataclass
import os


def _parse_bool(value, name, errors):
    if value is None or not value.strip():
        return False
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    errors.append(f"{name} must be true or false")
    return False


def _parse_number(value, name, default, minimum, maximum, errors, cast):
    if value is None or not value.strip():
        return default
    try:
        parsed = cast(value)
    except (TypeError, ValueError):
        errors.append(f"{name} must be a number")
        return default
    if not minimum <= parsed <= maximum:
        errors.append(f"{name} must be between {minimum} and {maximum}")
        return default
    return parsed


@dataclass(frozen=True)
class ArduinoConfig:
    enabled: bool = False
    port: str = ""
    baud_rate: int = 9600
    open_duration_ms: int = 3000
    serial_timeout_seconds: float = 0.25
    handshake_timeout_seconds: float = 3.0
    command_timeout_seconds: float = 2.0
    reset_wait_seconds: float = 1.8
    approval_max_age_seconds: int = 300
    configuration_error: str | None = None

    @classmethod
    def from_env(cls, environ=None):
        values = os.environ if environ is None else environ
        errors = []
        enabled = _parse_bool(values.get("AGASTYA_HARDWARE_ENABLED"), "AGASTYA_HARDWARE_ENABLED", errors)
        port = values.get("AGASTYA_ARDUINO_PORT", "").strip()
        baud_rate = _parse_number(values.get("AGASTYA_ARDUINO_BAUD"), "AGASTYA_ARDUINO_BAUD", 9600, 1200, 115200, errors, int)
        open_duration_ms = _parse_number(values.get("AGASTYA_SERVO_OPEN_MS"), "AGASTYA_SERVO_OPEN_MS", 3000, 1000, 30000, errors, int)
        serial_timeout = _parse_number(values.get("AGASTYA_SERIAL_TIMEOUT_SECONDS"), "AGASTYA_SERIAL_TIMEOUT_SECONDS", 0.25, 0.1, 5.0, errors, float)
        handshake_timeout = _parse_number(values.get("AGASTYA_SERIAL_HANDSHAKE_TIMEOUT_SECONDS"), "AGASTYA_SERIAL_HANDSHAKE_TIMEOUT_SECONDS", 3.0, 0.5, 10.0, errors, float)
        command_timeout = _parse_number(values.get("AGASTYA_SERIAL_COMMAND_TIMEOUT_SECONDS"), "AGASTYA_SERIAL_COMMAND_TIMEOUT_SECONDS", 2.0, 0.5, 10.0, errors, float)
        reset_wait = _parse_number(values.get("AGASTYA_ARDUINO_RESET_WAIT_SECONDS"), "AGASTYA_ARDUINO_RESET_WAIT_SECONDS", 1.8, 0.0, 5.0, errors, float)
        approval_max_age = _parse_number(values.get("AGASTYA_APPROVAL_MAX_AGE_SECONDS"), "AGASTYA_APPROVAL_MAX_AGE_SECONDS", 300, 30, 3600, errors, int)
        return cls(
            enabled=enabled,
            port=port,
            baud_rate=baud_rate,
            open_duration_ms=open_duration_ms,
            serial_timeout_seconds=serial_timeout,
            handshake_timeout_seconds=handshake_timeout,
            command_timeout_seconds=command_timeout,
            reset_wait_seconds=reset_wait,
            approval_max_age_seconds=approval_max_age,
            configuration_error="; ".join(errors) if errors else None,
        )
