from collections import deque
import unittest
from unittest.mock import Mock

from hardware.arduino_config import ArduinoConfig
from hardware.arduino_controller import (
    ArduinoServoController,
    HardwareProtocolError,
)


COMMAND_ID = "0123456789abcdef0123456789abcdef"


class FakeSerial:
    def __init__(self, *, answer_handshake=True, answer_release=True):
        self.is_open = True
        self.answer_handshake = answer_handshake
        self.answer_release = answer_release
        self.responses = deque()
        self.writes = []

    def write(self, payload):
        command = payload.decode("ascii").strip()
        self.writes.append(command)
        fields = command.split()
        if fields[0] == "PING" and self.answer_handshake:
            self.responses.append(f"READY {fields[1]}\n".encode("ascii"))
        elif fields[0] == "RELEASE" and self.answer_release:
            self.responses.append(f"ACK RELEASE {fields[1]}\n".encode("ascii"))
            self.responses.append(f"DONE {fields[1]}\n".encode("ascii"))
        return len(payload)

    def flush(self):
        pass

    def readline(self):
        return self.responses.popleft() if self.responses else b""

    def close(self):
        self.is_open = False


def enabled_config(**changes):
    values = {
        "enabled": True,
        "port": "COM7",
        "baud_rate": 9600,
        "open_duration_ms": 3000,
        "serial_timeout_seconds": 0.1,
        "handshake_timeout_seconds": 0.5,
        "command_timeout_seconds": 0.5,
        "reset_wait_seconds": 0,
        "approval_max_age_seconds": 300,
    }
    values.update(changes)
    return ArduinoConfig(**values)


class ArduinoControllerTests(unittest.TestCase):
    def test_hardware_is_disabled_without_opening_a_serial_port(self):
        serial_factory = Mock()
        controller = ArduinoServoController(ArduinoConfig(), serial_factory=serial_factory)

        self.assertFalse(controller.connect())
        self.assertFalse(controller.is_connected())
        self.assertFalse(controller.is_ready())
        self.assertEqual(controller.get_status()["state"], "disabled")
        serial_factory.assert_not_called()

    def test_site_activation_is_session_only_and_does_not_connect_automatically(self):
        serial_factory = Mock(side_effect=lambda *args, **kwargs: FakeSerial())
        controller = ArduinoServoController(ArduinoConfig(), serial_factory=serial_factory)

        enabled = controller.set_activation(True, "com7")

        self.assertTrue(enabled["enabled"])
        self.assertEqual(enabled["port"], "COM7")
        self.assertFalse(enabled["connected"])
        serial_factory.assert_not_called()

        self.assertTrue(controller.connect())
        serial_handle = controller._serial
        disabled = controller.set_activation(False, "COM7")
        self.assertFalse(disabled["enabled"])
        self.assertEqual(disabled["state"], "disabled")
        self.assertFalse(serial_handle.is_open)

    def test_site_activation_rejects_missing_or_non_com_ports(self):
        controller = ArduinoServoController(ArduinoConfig(), serial_factory=Mock())

        with self.assertRaises(ValueError):
            controller.set_activation(True, "")
        with self.assertRaises(ValueError):
            controller.set_activation(True, "COM0")
        with self.assertRaises(ValueError):
            controller.set_activation(True, "C:\\temp\\unrelated-file")
        self.assertEqual(controller.set_activation(False, "not-a-port")["state"], "disabled")

    def test_site_can_disable_gate_with_invalid_startup_configuration(self):
        config = ArduinoConfig(enabled=True, port="COM5", configuration_error="baud rate is invalid")
        controller = ArduinoServoController(config, serial_factory=Mock())

        with self.assertRaises(ValueError):
            controller.set_activation(True, "COM5")
        self.assertEqual(controller.set_activation(False, "")["state"], "disabled")

    def test_readiness_handshake_release_ack_and_timed_close(self):
        device = FakeSerial()
        controller = ArduinoServoController(enabled_config(), serial_factory=lambda *args, **kwargs: device)

        self.assertTrue(controller.connect())
        self.assertTrue(controller.is_connected())
        self.assertTrue(controller.is_ready())
        result = controller.release_panel(COMMAND_ID)

        self.assertEqual(result["status"], "closed_commanded")
        self.assertFalse(result["physical_position_verified"])
        self.assertIn(f"RELEASE {COMMAND_ID} 3000", device.writes)
        self.assertEqual(device.writes.count(f"RELEASE {COMMAND_ID} 3000"), 1)

    def test_bad_handshake_fails_closed(self):
        device = FakeSerial(answer_handshake=False)
        controller = ArduinoServoController(enabled_config(), serial_factory=lambda *args, **kwargs: device)

        self.assertFalse(controller.connect())
        self.assertFalse(controller.is_ready())
        self.assertFalse(device.is_open)
        self.assertIn("handshake", controller.get_status()["last_error"].lower())

    def test_disconnection_can_reconnect_on_a_later_attempt(self):
        device = FakeSerial()
        attempts = iter((OSError("port not found"), device))
        controller = ArduinoServoController(enabled_config(), serial_factory=lambda *args, **kwargs: next(attempts))

        self.assertFalse(controller.connect())
        self.assertTrue(controller.connect())
        self.assertTrue(controller.is_ready())

    def test_duplicate_commands_and_invalid_values_are_rejected(self):
        device = FakeSerial()
        controller = ArduinoServoController(enabled_config(), serial_factory=lambda *args, **kwargs: device)
        controller.connect()
        controller.release_panel(COMMAND_ID)

        with self.assertRaises(HardwareProtocolError):
            controller.release_panel(COMMAND_ID)
        with self.assertRaises(ValueError):
            controller.release_panel("not-a-command-id")
        with self.assertRaises(ValueError):
            controller.release_panel("fedcba9876543210fedcba9876543210", 30001)
        self.assertEqual(sum(line.startswith("RELEASE ") for line in device.writes), 1)

    def test_release_without_a_valid_ack_is_uncertain_and_not_retried(self):
        device = FakeSerial(answer_release=False)
        controller = ArduinoServoController(enabled_config(), serial_factory=lambda *args, **kwargs: device)
        controller.connect()

        with self.assertRaises(HardwareProtocolError):
            controller.release_panel(COMMAND_ID)

        self.assertEqual(controller.get_status()["last_command_status"], "uncertain")
        self.assertEqual(sum(line.startswith("RELEASE ") for line in device.writes), 1)

    def test_partial_serial_write_is_treated_as_an_uncertain_command(self):
        class PartialWriteSerial(FakeSerial):
            def write(self, payload):
                super().write(payload)
                return len(payload) - 1

        device = PartialWriteSerial()
        controller = ArduinoServoController(enabled_config(), serial_factory=lambda *args, **kwargs: device)
        self.assertFalse(controller.connect())
        self.assertFalse(device.is_open)
        self.assertIn("partially written", controller.get_status()["last_error"])


if __name__ == "__main__":
    unittest.main()
