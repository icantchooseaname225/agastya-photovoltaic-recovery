# Stage 1 software validation run — 19 November 2026

## Existing unit-test suite

The existing tests were run with the already-installed Python 3.14.10 interpreter using `python -m unittest discover -s tests -v`. No package was installed.

- 35 test cases were attempted; 29 passed and 6 errored during imports or dependency-backed checks.
- The unavailable packages were PyTorch (`torch`), NumPy (`numpy`) and Pillow (`PIL`). The missing imports affected the inference-device, thermal-image, image-import and numeric-estimator tests.
- `pytest` was not installed. The built-in `unittest` runner was used because the test files use `unittest.TestCase`.
- The documented PC-only end-to-end simulator, `tools/simulate_esp32.py`, was not run in this environment because it imports Pillow.

This is a partial software check, not a passing full-suite result. The passing cases cover dependency-free routing, ledger, provenance and dataset-contract behavior; the missing-dependency cases remain unverified here.

## Servo gate demonstration

Source inspection of `demos/servo_gate/agastya_eye_servo_gate_demo.ino` confirms synthetic serial commands for `APPROVE`, `REJECT` and `HOLD`, startup-to-HOLD behavior, a two-second HOLD timeout, and no new motion command for unknown or overlength input. The sketch remains separate from the classifier and is not a safety controller.

Arduino CLI 1.5.1 is bundled with the installed Arduino IDE, but the checked local data and sketchbook locations did not contain an Arduino AVR board core or the Servo library needed for this sketch. No board core/library was installed. A CLI metadata query fetched board/library catalog indices into its local cache outside the project; an attempt to remove those cache files was blocked by automatic tool review. The sketch was not compiled, and no board or servo was connected or tested.

## Validation boundary

No camera, ESP32-CAM, physical panel, sensor, robot, gate, laboratory process, assay or recovery test was performed. Results above describe only the local software run and source inspection.
