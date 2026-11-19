# Stage 1 Readiness

Reviewed 2026-09-26. Stage 1 is a laptop-assisted inspection prototype, not an autonomous sorter or an electrical safety tester. Do not begin Stage 2 until the physical capture path, operator workflow, and measurements below have been validated on real modules.

## Current status

- The laptop app, triage workflow, panel passport, and Stage 2-4 event API run on the PC. The protocol simulator passes, and the ESP32-CAM sketch compiles for the AI Thinker target.
- No ESP32-CAM serial port was identified for a physical upload, and no camera, electrical sensor, or real panel was exercised end-to-end. The current browser server is loopback-only; the ESP32 needs a separately started private-LAN server with a matching token.
- MobileNetV2 runs on the laptop, not on the ESP32. It is a screening aid; human review remains required.

## Local software check — 19 November 2026

The current Python 3.14.10 `unittest` run attempted 35 tests: 29 passed and 6 errored because PyTorch, NumPy and Pillow were unavailable. The documented PC-only simulator was not rerun because it also needs Pillow. See the [full validation record](STAGE1_VALIDATION_RUN_2026-11-19.md). This partial result does not supersede the earlier simulator record above or demonstrate camera, panel, model-field or hardware validation.

## Remaining blockers and fixes

| Priority | Gap | Fix and completion evidence |
|---|---|---|
| Blocker | Camera and upload path have not been tested on the actual board. | Connect the AI Thinker board, flash the sketch, then complete repeated capture/upload/retry tests. Save the board model, camera sensor, firmware build, and sample images with the test record. |
| Blocker | No local field images from the panels EYE is meant to inspect. | Use a repeatable camera position, focus, background, and lighting. Give each physical panel one stable ID; capture a full-panel view and close-ups, and keep every view of that panel in one data split. Include clean, soiled, damaged, shaded, varied-angle, and varied-light cases as actually observed. |
| Blocker | The RGB model does not cover important defect classes. | The visible-light checkpoint has only `clean`, `dust`, `bird_drop`, and `other`. Its 734 images come from one public source and form 433 filename/hash-linked groups, not 433 confirmed physical panels. Its RGB training data has no `crack`, `broken`, `burned`, or `snow` examples. Collect and independently verify these labels before expanding the RGB model. |
| Blocker | Image classification does not locate damage or establish severity. | RaptorMaps is a separate 24x40 thermal-crop classifier. PV-Multi-Defect is grayscale camera-crop data with boxes (`broken`, `hot_spot`, `black_border`, `scratch`, `no_electricity`); its source sensor band is unspecified, EYE reduces boxes to image-level hints, its image-data license is undeclared, and it has no `burned` class. Keep it separate from full-panel AI Thinker RGB. For operational crack/burn/extent decisions, obtain rights-cleared full-module data, train a detector on verified boxes, and evaluate by held-out physical panels. Do not infer electrical defect or severity from pixels. |
| Blocker | Electrical telemetry has no sensor calibration or panel validation. | First use only the listed 3 V demo panel, INA219, resistor, and multimeter. Compare readings against the meter at several low-voltage operating points and record instrument, wiring, and calibration. Do not attach this kit to a full-size module/string. A real module test needs a suitably rated PV I-V tester and qualified procedure. |
| Before field use | The current HTTP upload is plain text on the LAN. | Keep the service bound to a trusted isolated private network, use a long random token on both laptop and firmware, allow only the private Windows Firewall profile, and never port-forward it. |
| Before Stage 2 | Triage still depends on entered technology/dimensions and operator disposition. | Test all route priorities with known panels and ambiguous cases. Keep unknown technology, uncertain damage, missing electrical evidence, or any disagreement in human review. No visual-clean result should automatically approve reuse or activate machinery. |

## Model status and next training cycle

The full-panel visible-light held-out set has 104 images: accuracy 84.6% and macro-F1 83.5%. Its checkpoint currently predicts only `clean`, `dust`, `bird_drop`, and `other`. These are internal results from one public source, not expected field performance. Some source annotations refer to 125 files missing from the archive; provenance is retained in `datasets/import_reports/` and the processed manifest. The RGB classifier does **not** predict crack/burn or a severity score and does not localize damage; manually confirmed structural defects remain safety holds. The corrected PV-Multi-Defect crop model scored 70.0% macro-F1 on its 148-image test split; `broken` F1 is 52.6% (62.5% precision, 45.5% recall). This split is image-hash grouped, not panel-independent; neither this nor the RaptorMaps thermal experiment is validated for operational sorting. The earlier misidentified-modality checkpoint is superseded.

A separate CC BY 4.0 Mendeley research dataset (`10.17632/pxyzzkbs4b.1`) is imported at `datasets/raw/pv_el_hdr_bw_v1/`: 84 progressive conditions, 252 paired visible-HDR/BW-near-IR/EL images, controlled electrical measurements, descriptions, and source damage boxes. Three separate frozen ImageNet MobileNetV2-feature plus ridge regression runs predict measured power-loss percentage, each using leave-one-cell-out evaluation. Results: HDR MAE 13.64 percentage points (R² 0.27), BW 13.81 (R² 0.22), and EL 18.04 (R² 0.27); the training-cell-mean predictor is 19.71 MAE points. There are only **two physical cells**, so these are reproducible exploratory baselines, not independent field validation. Source annotations include crack descriptors on 11 rows and burn/soot/melting words on 18 rows; these are small row counts, not 11/18 independent panels. The app now displays the matching BW/NIR and EL regression outputs as research-only sidecar fields, but never uses them in live full-panel triage, sort routes, or actuator control; they are not ESP32/INA219 measurements. The report and predictions are in ignored `datasets/processed/pv_degradation_benchmark/`; the modality models remain explicitly research-only.

The current candidate already trains for up to 30 epochs with early stopping and class-weighted loss. More epochs on these same images will not supply missing defect examples and risk fitting to the same source. Do not choose a new model by repeatedly consulting the 104-image test set. Next training cycle:

1. Capture real target-camera images and label them after operator inspection; use physical panel ID to group every repeat/crop.
2. Keep a locked test set from different panels (preferably a later date or different collection site). Use training/validation only for model and threshold selection.
3. Compare the four-class baseline using per-class precision/recall/F1, confusion matrix, calibration, and false-negative review. Add a class only when it has adequate independent panels in all splits.
4. Add localization only with verified boxes/masks. PV-Multi-Defect boxes are retained, but its current model predicts image-level visible-crop labels only; the dataset-specific license is undeclared. It establishes neither a burn class, severity, calibrated temperature, electrical state, nor localization. Keep thermal and EL data separate from visible RGB until matching hardware, clear rights, labels, and evaluation exist.
5. Export only human-confirmed labels with `py training/export_reviewed.py`, rebuild group splits, then train using the commands in the main README. Preserve the old checkpoint until the candidate passes the locked evaluation.

For the separate severity benchmark, run `py training/import_pv_degradation.py` followed by `py training/train_pv_severity.py --modality HDR`. BW and EL are distinct experiments. The benchmark is also shown in the app's Training data view when its report exists. No severity is displayed for live panel captures until a model is trained and externally validated on the actual camera and matched electrical tests.

Potential datasets are not interchangeable: ELPV consists of electroluminescence cell crops and its images are CC BY-NC-SA 4.0, not visible full-panel RGB. SolarFCD combines RGB/drone and thermal imagery; its public repository documents MIT for code but does not make the component image licenses clear in its README. Do not merge either into the RGB training set without checking the exact data terms, modality, source groups, and labels.

## Stage 1 demonstration hardware

This is a **low-voltage tabletop demo**, assuming the AI Thinker ESP32-CAM and laptop are already owned. Indicative listed subtotal is approximately **₹1,311-₹1,320 before shipping**; confirm seller prices and availability before ordering.

| Item | Approx. cost | Purpose / limit |
|---|---:|---|
| ESP32-CAM-MB USB programmer, only if no adapter is available | ₹85 | Upload firmware to the existing ESP32-CAM. |
| INA219 breakout | ₹229 | Optional voltage/current/power telemetry for the low-voltage demo only. |
| Mini solar panel, 3 V / 0.45 W | ₹156 | Safe small source for the bench exercise. |
| Basic digital multimeter | ₹699 | Independent low-voltage cross-check. |
| Breadboard, jumper leads, 100-ohm 0.25 W resistor | about ₹142-₹151 | Temporary wiring and small dummy load. |
| Existing AI Thinker ESP32-CAM and laptop | ₹0 incremental | Camera sends images; laptop runs app/model/database. |

No RGB-IR camera, thermal imager, full-size PV tester, robot, conveyor, or actuator is included. The INA219 adapter reports raw readings as `not_tested`; it never certifies a panel. The INA219 I2C wiring uses GPIO13/14, which are shared with microSD, so do not use the SD interface at the same time. Full-size PV panels can exceed the breakout, breadboard, and ESP32 limits; do not connect them to this kit.

## Upload to the ESP32-CAM

Only the firmware is uploaded to the ESP32. The Python app, MobileNet checkpoint, data, and triage run on the laptop.

1. Use an ESP32-CAM-MB programmer, or a USB-to-serial adapter wired for 5 V board power and 3.3 V UART logic. With a serial adapter, cross TX/RX, connect GND, hold GPIO0 to GND during reset/upload, then remove that jumper and reset to run. Never feed 5 V logic into an ESP32 GPIO.
2. In Arduino IDE install/select **esp32 by Espressif Systems**, board **AI Thinker ESP32-CAM**, upload speed 115200, and the COM port for the board. A workspace PATH check on 10 October 2026 did not find `arduino-cli`, so its local installation and the Espressif core must be confirmed before relying on command-line flashing. See Espressif's [Arduino-ESP32 setup guide](https://docs.espressif.com/projects/arduino-esp32/en/latest/installing.html).
3. In PowerShell, from the project root, create the private configuration file:

   ```powershell
   Copy-Item .\firmware\agastya_eye\secrets.example.h .\firmware\agastya_eye\secrets.h
   ```

   Put the Wi-Fi name/password, stable device ID, laptop's private IPv4 address (from `ipconfig`), and one random token into `secrets.h`. It is ignored by Git; do not paste or publish it.
4. Start the device API on the laptop using the same token. Use a trusted private Wi-Fi network and keep the terminal open:

   ```powershell
   $env:AGASTYA_DEVICE_TOKEN = ([guid]::NewGuid().ToString('N') + [guid]::NewGuid().ToString('N'))
   py app.py --host 0.0.0.0 --port 8773
   ```

   Copy that token into firmware `DEVICE_TOKEN`; set `LAPTOP_BASE_URL` to `http://<laptop-private-ip>:8773`. Permit private-network access in Windows Firewall if prompted. Plain HTTP is not suitable for a public network.
5. Open `firmware/agastya_eye/agastya_eye.ino` in Arduino IDE, compile/upload, and open Serial Monitor at 115200 baud with newline enabled. Run `status`, enter the panel fields (`panel=...`, `tech=c_si`, dimensions and junction location when known), then send `capture`. Confirm the response in Serial Monitor and the new panel record in the laptop app.
6. If upload cannot sync, verify the COM port/USB data cable and power. On a serial adapter, repeat bootloader entry with GPIO0 grounded while resetting; after a successful upload, disconnect GPIO0 and reset.

## Gate before Stage 2

- A real ESP32-CAM repeatedly captures and uploads correctly on the private LAN, with no secrets committed.
- Operators can create a panel record, inspect full and close-up evidence, correct metadata, review the route, and export its passport.
- At least one low-voltage sensor run is cross-checked against the meter, with calibration/provenance recorded; electrical outcome remains `not_tested` unless a qualified human performs a separate approved procedure.
- The candidate model is evaluated on panel-disjoint field data, class-wise errors are reviewed, and uncertain/unknown cases hold for a person. Do not treat benchmark accuracy as readiness for automated sorting.
- Stage 2 de-framing has its own guarded fixture, isolation procedure, and safety controls. EYE's route/event API is a handoff record, not authorization to operate machinery.
