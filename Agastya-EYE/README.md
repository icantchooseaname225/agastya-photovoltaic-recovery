# Agastya-EYE

Agastya-EYE is the first inspection stage of the Agastya panel-recovery workflow in [Agastya_Thesis.docx](../08_Reports/Technical_Reports/Agastya_Thesis.docx): photograph and record a module before any destructive processing. The AI Thinker ESP32-CAM captures and uploads; the laptop runs the operator app, experimental vision classifier, triage rules, and SQLite material-passport ledger. Voltage/current telemetry is a separate optional sensor path. The camera alone cannot measure electricity.

In the current four-stage charter, EYE supports Stage 1 inspection, intake records, and routing; it is not a silver-recovery operation. The current numbered stages are Stage 1 vision-based triage, Stage 2 robotic mechanical disassembly, Stage 3 hot-knife/foam-roller thermal separation, and Stage 4 material liberation, separation and silver recovery. The robotic-arm and foam-roller directions are design concepts; EYE does not control them. Stage 4 route selection remains open. EYE does not control process equipment, and its computer-vision results do not verify silver content or recovery. Use the root current architecture when older files use another map.

## Synthetic servo control-interface demo

The original, uncompiled tabletop interface sketch accepts synthetic `APPROVE`, `REJECT`, and `HOLD` commands. It remains separate from the classifier and the Arduino integration. See [the demo notes](demos/servo_gate/README.md).

## Run the laptop app

For the normal PC demo, double-click `Start-EYE.bat`. It finds an available local port, starts the app in the background, waits for the API, and opens the browser. If startup fails, it shows the log file path. The launcher reuses an EYE server already running on its selected port.

From a PowerShell prompt, invoke the launcher without changing the machine's execution policy with `powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Start-EYE.ps1`.

The launcher selects an interpreter that can import the application dependencies, prints its runtime versions, and stores a PID record for servers it starts. Use `powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Stop-EYE.ps1` to request a clean local shutdown. `GET /api/ping` is a liveness check; `GET /api/v1/health` reports database/model readiness and returns a non-ready status if the primary database or RGB model is unavailable.

The launcher checks, in order, an explicitly configured `AGASTYA_EYE_PYTHON`, the project `.venv`, user-managed virtual environments under `%USERPROFILE%\Envs`, Python Launcher Python 3.14, then the launcher's default Python. It selects only an interpreter that imports Pillow, NumPy, PyTorch, torchvision, and pySerial, and prints the selected interpreter. The app's status banner and `/api/v1/health` report the active CUDA device and model status. To point EYE at another existing compatible interpreter, set `AGASTYA_EYE_PYTHON` to its `python.exe` path before launching. No second PyTorch or CUDA installation is required when the existing environment passes this check.

## Arduino Uno/Nano servo gate

The optional SG90 gate uses the separate `hardware/` serial controller and `firmware/servo_gate/servo_gate.ino`. The classifier and inspection pipeline never send hardware commands. Activation defaults to disabled; after wiring and uploading the firmware, enter the detected Uno/Nano COM port and enable the current session in the site's **Arduino Gate** panel. The app accepts a release only after an operator has recorded a final approved `REUSED` result for a fresh, high-confidence clean c-Si RGB inspection with a documented electrical pass, then separately enters their ID and confirms the panel ID in the gate control. Rejected, uncertain, incomplete, stale, and human-review-pending records remain blocked. See [the Arduino setup, wiring, configuration, and demonstration guide](docs/ARDUINO_SERVO_GATE.md) and [the firmware notes](firmware/servo_gate/README.md).

The app distinguishes an inspection result from the Arduino's release/close acknowledgements. The SG90 has no position sensor here, so the software cannot confirm actual servo or barrier movement. Hardware command failures are recorded as uncertain and are not retried for the same inspection. The pre-existing [synthetic serial demo](demos/servo_gate/README.md) remains available for its original `APPROVE`/`REJECT`/`HOLD` interface.

To run the server directly in PowerShell and see live logs, set `AGASTYA_EYE_PYTHON` to a compatible interpreter's `python.exe` path, then run:

```powershell
$env:AGASTYA_EYE_PYTHON = "C:\path\to\compatible\python.exe"
& $env:AGASTYA_EYE_PYTHON .\app.py
```

The three PyTorch image classifiers use CUDA automatically when the selected PyTorch build can initialize the GPU. Set `AGASTYA_EYE_DEVICE=cpu` to force CPU inference, or `AGASTYA_EYE_DEVICE=cuda` to require CUDA; the default `auto` mode reports and falls back to CPU if CUDA cannot initialize or inference fails. Check `/api/v1/health` for the active device and model status.

Open the address printed by the launcher (normally `http://127.0.0.1:8765`; if that port is occupied, the launcher selects and prints another available port). The operator app can upload a photo, fetch the ESP32 `/capture` endpoint on a private LAN, or connect to a computer/USB webcam using the browser’s camera permission. Webcam access requires localhost or HTTPS; click **Start webcam**, allow access, then capture a frame. The app records the frame in the same inspection flow as an upload. It stores images in `images/` and history in `database/eye.sqlite3`. Each panel has a versioned JSON material passport at `/api/v1/panels/<panel-id>/passport`, including inspection images, camera modality/view/sensor/capture-group provenance, technology, measured frame dimensions, nameplate rating, junction-box location, electrical-test provenance, separate recommended/final sort routes, reviewer decisions, and Stage 2-4 process events. Schema 1.6 passports hash the capture-view field while retaining verification support for older inspection hashes.

### Webcam image quality

Use the app in current Chrome or Edge if the embedded browser does not list a camera. In Windows, close Camera, Teams, Zoom, and other apps that may hold the webcam; check **Settings → Privacy & security → Camera** and allow desktop apps; then reload EYE, press **Start webcam**, and grant access for `127.0.0.1`. The camera selector appears after browser permission is granted. Select the USB webcam explicitly and try 1080p, then 720p if the device cannot supply that mode. The readout is the actual stream resolution, not the requested one. A blocked or indefinitely pending prompt usually means browser permission, device contention, or that the embedded browser cannot expose hardware; use Chrome/Edge at the same local URL.

Bad optics cannot be repaired in software: upscaling or sharpening invents pixels and can hide cracks. For better evidence, clean the lens, use bright diffuse light and avoid reflections, brace the camera, fill the frame without cropping the panel edges, and capture a full-panel overview plus close-ups where defects are visible. Use the camera/driver's real focus or optical zoom when supported; the controls are shown only when the device exposes them. EYE displays actual captured dimensions and gives indicative dimness, clipping and edge-detail warnings. These checks are not a calibrated image-quality score. If the webcam is genuinely low resolution or cannot focus close, a 1080p autofocus USB webcam or a phone camera transferring original photos is the effective upgrade; EYE preserves the received detail but cannot create missing detail.

EYE's first-stage result combines visual evidence with measurements recorded by an operator or a future rated sensor station. The camera cannot measure voltage/current or infer real-world dimensions by itself: enter dimensions measured with a tape/caliper and electrical readings from an appropriately rated instrument. EYE calculates outer frame area from dimensions, calculates watts as V×I when no power reading is entered, and can compare that snapshot with the module nameplate rating. That comparison is not corrected for irradiance, temperature, orientation, or test conditions and is not a degradation diagnosis. The destination shown in the app is a recommendation for a person or future PLC interface; no actuator is connected or commanded.

The saved inspection now displays a simple three-way tabletop lane result: left for a second-life candidate with documented c-Si electrical pass, right for an isolated c-Si Stage 2 route, and hold for all other cases. A visual-model `other` confidence strictly above 50% raises a **potentially broken** safety-hold flag and requires physical operator confirmation before choosing a process route. `Other` is a broad, unverified class that can include damage, scratches, and other conditions; it does not prove the panel is broken. This is a dry run only; no arm command is sent. See the [Stage 1 sorter build guide](docs/STAGE1_SORTER_BUILD.md) for the sensor path, current limitations, and sub-₹1,000 arm parts.

### Stage walkthrough

Choose **How stages work** in the app to see Stage 2 preparation, Stage 3 front-glass separation, and a Stage 4 silver-removal route gate. The route gate leaves the method and product form open; it does not imply a selected machine. The drawings explain a proposed material path, not equipment operation or performance. No stage machine or recovery result is validated.

### First PC test

1. Double-click `Start-EYE.bat` and wait for the browser to open.
2. Upload a panel photo (or enter an ESP32 snapshot URL), choose `Visible RGB · full panel`, and enter a stable panel reference if available.
3. Enter dimensions only after measuring them physically. Leave technology as unknown if it is not verified. Keep electrical result at `Not tested` unless a separate instrument and qualified procedure produced the reading.
4. Save the inspection. EYE assigns a panel ID and shows the route, destination recommendation, and evidence. Unknown or incomplete inputs stay in review; no lane is physically actuated.
5. Open `Training data` to inspect source mappings, model versions, evaluation, and limitations.

To expand RGB training with relevant images, collect actual webcam captures of the panels and defect types EYE will inspect. Use a stable panel/capture-group reference for every overview and close-up, and select a human-confirmed visual class only when supported by inspection. Keep all views from one physical panel in one split. Export reviewed captures using `py training/export_reviewed.py`; inspect its manifest before training. Public web images with uncertain labels, and EL/NIR/thermal images, are not interchangeable with RGB webcam evidence.

One additional candidate, [SOLAR PANEL DEFECT by Solar Panel Defects](https://universe.roboflow.com/solar-panel-defects-ax0gw/solar-panel-defect-w1dfi), declares CC BY 4.0 and object-detection labels for broad visible faults. Its project page and version details report different image totals; it is not yet imported. Verify the chosen export version, annotations, source-panel grouping, overlap and attribution before training. The current classifier remains unchanged until that intake is complete.

## Upload to AI Thinker ESP32-CAM

1. Install the **esp32 by Espressif Systems** board package in Arduino IDE Boards Manager. If it is not listed, add `https://espressif.github.io/arduino-esp32/package_esp32_index.json` in Preferences first. Choose **AI Thinker ESP32-CAM** and a stable upload speed such as 115200. Espressif documents setup [here](https://docs.espressif.com/projects/arduino-esp32/en/latest/installing.html).
2. To upload, use an ESP32-CAM-MB USB programmer if you have one. Insert the camera module in the correct orientation, connect a data-capable USB cable, and select its COM port. If using a USB-to-serial adapter instead, follow its pinout: supply the ESP32-CAM at 5 V with adequate current, share GND, cross TX/RX, use 3.3 V UART logic, connect GPIO0 to GND while entering the bootloader, reset/upload, then disconnect GPIO0 from GND and reset to run. Do not wire the USB-UART 5 V logic signal to an ESP32 GPIO.
3. Copy `firmware/agastya_eye/secrets.example.h` to `firmware/agastya_eye/secrets.h`. Fill in the Wi-Fi name/password, a stable device ID, the laptop's private Wi-Fi IPv4 address from `ipconfig`, and a strong API token. `secrets.h` is git-ignored.
4. In PowerShell, start the device-enabled app on the local network:

   ```powershell
   powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Start-EYE.ps1 -ForDevice
   ```

   The launcher selects an available port and prints a token, stored outside the project at `%LOCALAPPDATA%\Agastya\EYE\device-token.txt` so later starts keep matching the flashed firmware. Copy it into `DEVICE_TOKEN`; set `LAPTOP_BASE_URL` to `http://<laptop-private-ip>:<printed-port>` using the private IPv4 address from `ipconfig`. Allow private-network access in Windows Firewall if prompted. Keep the app and ESP32 on the same trusted Wi-Fi. The API uses plain HTTP: never expose it with port forwarding or use it on a public network.
5. Open `firmware/agastya_eye/agastya_eye.ino` in Arduino IDE and upload. Open Serial Monitor at 115200 baud with newline enabled. Type `status`, set a stable `panel=<asset-reference>`, and choose `view=front`, `view=rear_nameplate`, `view=rear_junction_box`, or `view=rear_overview` before each capture. Flip the same small panel and capture each side using the same panel reference; EYE appends them to that panel's passport with their view labels. Read the nameplate yourself, then set `tech=c_si|thin_film|other|unknown` and `rated=<W>` only as verified. Enter physically measured `width=<mm>` and `height=<mm>` and `junction=rear_center|rear_upper|rear_lower|rear_left|rear_right|other|unknown` when known. Send `capture`. Settings persist across restarts. `panel=clear` clears the stored reference and associated measurements; `width=clear`, `height=clear`, and `rated=clear` clear those values (width and height must be both set or both cleared).

### Build or upload from PowerShell

Arduino IDE is enough for routine upload. On this PC, stable Arduino CLI 1.5.1 and Espressif ESP32 core 3.3.12 are installed in the same Arduino15 package store used by the IDE; the AI Thinker target is `esp32:esp32:esp32cam`. Arduino CLI is optional for repeatable builds; its official documentation is [here](https://docs.arduino.cc/arduino-cli/). With the CLI installed at `D:\Arduino\Arduino CLI\arduino-cli.exe`, use:

```powershell
$cli = 'D:\Arduino\Arduino CLI\arduino-cli.exe'
& $cli core list
& $cli compile --fqbn esp32:esp32:esp32cam --build-path "$env:TEMP\agastya-eye-build" .\firmware\agastya_eye
& $cli board list
& $cli upload --fqbn esp32:esp32:esp32cam --port COM7 .\firmware\agastya_eye
```

Replace `COM7` with the ESP32-CAM's actual port. On another PC, add the Espressif stable board index in Arduino IDE Preferences/Boards Manager, or configure it once in CLI with `& $cli config add board_manager.additional_urls 'https://espressif.github.io/arduino-esp32/package_esp32_index.json'`, then run `& $cli core update-index` and `& $cli core install esp32:esp32@3.3.12`. The build requires your local `secrets.h`; it is intentionally not committed.

The device endpoint is `POST /api/v1/inspections`. It records device ID, optional capture time and panel reference, image, camera modality, capture view, sensor ID and capture group, panel technology, manually entered dimensions/junction-box position, and optional raw electrical readings. The ESP32 firmware sends `visible_rgb`. Near-infrared reflectance and electroluminescence are retained without inference. A distinct `thermal_infrared` stream can use the research-only thermal classifier; its outputs never replace calibrated temperature, voltage, or current readings. Device uploads cannot assert electrical pass/fail; the laptop UI requires readings, test procedure, instrument ID, and operator for a human-entered result. That is a recorded operator attestation, not an electrical certification. Request IDs make retries idempotent. The laptop API token and images travel over plain HTTP: use only a trusted isolated LAN, keep the token private, and never port-forward this prototype to the internet.

Later stations append measured events with `POST /api/v1/panels/<panel-id>/events`. Events require a timezone-aware timestamp, station/operator identity, measurement units, and instrument/calibration provenance. Units include `J`, `Wh`, `kWh`, `s`, `min`, and `rpm` for energy and elapsed time. The rpm unit remains generic for a future route that may need it; no Stage 4 rotor or machine is selected. The API enforces EYE isolation/route before Stage 2, then Stage 2 completion before Stage 3, and Stage 3 completion before Stage 4. It is a measurement/passport interface only; it does not issue machine commands. See [Stage interoperability](docs/STAGE_INTEROP.md) for the payload and the staged safety boundary.

The sketch uses Espressif's maintained [ESP32 camera driver](https://github.com/espressif/esp32-camera). The laptop can also fetch a camera snapshot through the UI if the ESP32 CameraWebServer example is flashed separately; the included uploader instead sends a snapshot directly to the authenticated laptop API.

## Models and limits

The AI model is **MobileNetV2** from TorchVision, initialized with ImageNet weights and fine-tuned on the laptop's CPU (classifier head plus the last feature block by default). It does not run on the ESP32-CAM. Its checkpoint is CPU-compatible. The current public-data model uses four broad classes: `clean`, `dust`, `bird_drop`, and `other`. `electrical` and `physical` source labels, plus multi-label images, were conservatively grouped into `other`; this is not crack/burn localization, panel-technology identification, an electrical test, or a reuse decision.

The current RGB candidate's group-aware held-out test contains 104 images: 84.6% accuracy and 83.5% macro-F1 (baseline: 83.7% and 80.1%). Per-class results are mixed: `bird_drop` F1 is 72.7% versus the prior checkpoint's 82.9%, so confidence thresholds and human review remain essential. The RGB model has no trained crack/burn classifier or localization and does not estimate severity. This is a small internal benchmark, not field accuracy. The first dataset is a single public GitHub derivative; 125 of 866 annotated records referenced by its COCO files were absent from the downloaded archive. Exact image hashes, group-aware split, source/license mappings, and missing-file list are recorded under `datasets/`. Capture and label panels from the actual target environment before using it to make operational decisions. Frame dimensions and junction-box location are explicitly entered measurements, never estimates from pixels.

### Thermal infrared research classifier

EYE now includes a separate MobileNetV2 thermal classifier trained from RaptorMaps' MIT-licensed `InfraredSolarModules` archive. Its 20,000 source samples are 24x40 grayscale thermal crops with 12 labels; 19,972 unique images are in its image-level train/validation/test split after 12 conflicting-label records were excluded. Its classes include `cracking` and hotspot states, but **not separate `burned` or `broken` labels**. There are no boxes, calibrated temperatures, or severity targets. Because physical-module IDs are not present, the held-out score is not panel-independent or field accuracy. A high-confidence `cracking` output requests safety hold and human physical review; all other thermal predictions remain advisory and cannot trigger Stage 2. The model runs on the laptop, never on the ESP32.

Import and train it separately from RGB:

```powershell
py training/import_raptormaps_thermal.py
py training/train_thermal_classifier.py --epochs 6 --batch-size 64 --threads 4
```

The importer verifies the pinned archive SHA-256, retains original class names, writes an ambiguity audit, and keeps exact duplicate pixels in one split. The thermal model and its evaluation are written to `models/solar_thermal_mobilenet_v2.*`; the Data page shows its image-level metrics and limitations. See [the thermal model card](docs/THERMAL_MODEL_CARD.md) for source attribution, class definitions, evaluation caveats, and the field-data gate.

### Visible close-up defect research model

The separate [PV-Multi-Defect](https://github.com/CCNUZFW/PV-Multi-Defect) source contains camera-captured crops processed to grayscale; the originating paper does not specify sensor band, while later publications call it infrared. Treat source modality as unverified, not as calibrated thermal data or guaranteed RGB-equivalent full-panel imagery. It describes 1,108 crops and box labels for `broken`, `hot_spot`, `black_border`, `scratch`, and `no_electricity`; there is no `burned` class. The repository does not declare a dataset-specific image license, so the downloaded copy and derived checkpoint are retained locally for research only pending permission. EYE excludes 60 exact-image groups with conflicting boxes and makes a grouped 689/148/148 image split. The separate MobileNetV2 screen converts retained boxes to image-level labels, so it does not localize defects. Its outputs are stored as advisory-only evidence and never affect the sort recommendation. It accepts square, high-resolution close-ups only, and transfer from the source optics to the RGB camera is unvalidated.

```powershell
py training/import_pv_multi_defect.py
py training/train_surface_defect_classifier.py --epochs 12 --batch-size 32 --threads 4
```

The model and held-out report are saved as `models/solar_grayscale_crop_surface_defects_mobilenet_v2.*`; the Training Data page shows its split metrics, broken-label precision/recall, and license status. The fresh 148-image test split scored 70.0% macro-F1; `broken` F1 is 52.6% (62.5% precision, 45.5% recall). Read the [visible close-up model card](docs/VISIBLE_CROP_MODEL_CARD.md) and [dataset source notes](datasets/SOURCES.md) before using or sharing these artifacts. The scores are image-level, not physical-panel-independent field validation. A `hot_spot` source label is not proof of a burn, and none of these scores measures severity, temperature, voltage/current, or panel reuse value. The model does not authorize a sort lane.

### Separate crack, burn, and severity research set

The CC BY 4.0 [PV_EL_HDR_BW_Test_DB](https://data.mendeley.com/datasets/pxyzzkbs4b/1) contains 84 progressive damage conditions on only two physical cells, with 252 paired visible-HDR, monochrome near-IR/BW, and EL images. Its CSV records visual damage descriptions/boxes and measured power-output loss under a controlled lamp. It includes crack and fire/thermal-damage examples, but it is not a full-module ESP32 camera dataset. Keep modalities separate, preserve the DOI attribution, and never treat the regression output as a reading from EYE's camera or INA219.

The app exposes NIR-BW and EL power-loss estimates as a separate research-only field, with the source sample count and warning. RGB, thermal, and close-up inputs do not receive this estimate. It is never used by triage or sorting. The additional user-requested Roboflow, Hugging Face, and GitHub sources have not been merged or trained: Roboflow requires authenticated export, the Hugging Face endpoint returned 401, and some GitHub links are code/weights rather than reusable image datasets. See [dataset source and intake status](datasets/SOURCES.md) before importing them.

The importer checks the pinned v1 archive SHA-256 and extracts into the separate ignored research-data folder. The benchmark extracts frozen ImageNet MobileNetV2 embeddings and trains a small ridge regressor for measured power loss; it evaluates by holding out an entire physical cell in turn. Run:

```powershell
py training/import_pv_degradation.py
py training/train_pv_severity.py --modality HDR
```

If the archive is not present, append `--download` to the import command. Separate BW or EL experiments can be run with `--modality BW` or `--modality EL`; do not combine modalities into one input. The three experiments all have 84 paired rows and two cell-held-out folds: HDR MAE 13.64 percentage points (R² 0.27), BW 13.81 (R² 0.22), and EL 18.04 (R² 0.27), compared with a 19.71-point training-cell-mean predictor. This modest signal is not independent validation: images are laboratory cell close-ups, and only two physical cells exist. Reports/predictions are written under `datasets/processed/pv_degradation_benchmark/`; research-only artifacts and metadata are written under `models/`. Only the matching NIR-BW and EL artifacts are loaded by the separate research-estimate field; they never affect live EYE triage. The report applies separate source thresholds to soiling rows instead of forcing them into the mechanical/thermal damage scale.

The full-panel RGB model continues to produce only the classes listed in its checkpoint (currently `clean`, `dust`, `bird_drop`, and `other`). Operators can record a visually confirmed `crack`, `broken`, or `burned` condition, which routes to a safety hold, but this RGB checkpoint does not detect those labels or locate damage. The separate close-up screen includes `broken` and `scratch` hints, but no `burned` class, and cannot change routing. Before enabling automated severity or defect localization, collect multiple independently sourced, uniquely identified full modules with matching calibrated electrical measurements and verified boxes/masks. Keep whole physical panels and repeat views within one train/validation/test group, and lock a site- or time-separated final test set.

The Stage 1 sort routes are `HUMAN_REVIEW`, `SAFETY_HOLD`, `ELECTRICAL_TEST_REQUIRED`, `SERVICE_AND_RETEST`, `SECOND_LIFE_REVIEW`, `STAGE_2_CSI`, and `LICENSED_THIN_FILM_HANDLER`. The algorithm recommends a route; a separate operator disposition stays `PENDING_REVIEW` unless a person records an outcome. Unknown panel technology remains in review, thin-film panels remain intact for the licensed-handler route, and electrical failure or confident/operator-confirmed structural damage takes priority as a safety hold. Operator-confirmed soiling recommends service and retest. A clean visual result alone never approves reuse. Stage 2 routing requires confirmed c-Si, a recorded isolation check, and an operator note. Route and disposition overrides are audited. The hash chain detects record/image changes but is not a signed identity system and cannot prevent an administrator from rewriting the local database. Nothing in this prototype is a safety certification or recycling determination.

## Later-stage hand-off

The material passport is the hand-off record, keyed by stable `panel_id`. Stage 2-4 station events now append measured outputs and process provenance without rewriting EYE evidence. Keep the current AI Thinker camera for the ₹2,000 demonstration stage; a supposed RGB+IR ESP32-CAM is not a safe assumption. The existing OV2640-class setup remains the visible RGB node. A near-IR, thermal, or EL channel is a separate identified sensor stream paired by `capture_group_id`; EYE does not fuse these signals. Thermal inference currently requires a separate uploaded thermal camera image and is not produced by the AI Thinker camera. Thermal images are not calibrated temperature measurements. Hardware and robot-control limits are detailed in [Stage interoperability](docs/STAGE_INTEROP.md).

## GitHub dataset and training

The importer pins commit `868cf7c004cf3cea274d2bfdf398ac6c2216ca47` of [solar-panel-inspection-dataset](https://github.com/IsuruMunasinghe98/solar-panel-inspection-dataset). The authors say the dataset is CC BY 4.0 and require attribution to both their team and the original `solarpaneldataset` source; preserve that attribution if redistributing data or derived models. Import and train with:

```powershell
py training/import_github_inspection.py
py training/prepare_dataset.py --overwrite
py training/train_classifier.py --epochs 30 --batch-size 16
```

The importer caches the pinned source ZIP in `datasets/.cache/`, imports only annotated valid images, hashes duplicates, and links filename families to prevent split leakage. The preparation step places whole groups in train/validation/test and keeps provenance in `datasets/processed/processed_manifest.csv`. Training class-balances the loss, augments only the training split, fine-tunes MobileNetV2's last feature block, early-stops on validation loss, and writes held-out metrics to `models/solar_mobilenet_v2.json`. After inspecting real modules, optionally mark **Human-confirmed visual class** in the app. Export those reviewed images and rebuild the group-aware splits with:

```powershell
py training/export_reviewed.py
py training/prepare_dataset.py --overwrite
py training/train_classifier.py --epochs 30 --batch-size 16
```

Only human-confirmed image labels are exported; model predictions and final sorting decisions are not used as labels. Repeated images and captures of the same panel are kept in one data split. Install the dependencies from `requirements.txt` first. Dataset candidates, attribution, and modality/license decisions are documented in `datasets/SOURCES.md`; do not merge electroluminescence crops into the RGB camera task.

## Stage hardware under ₹2,000

The user already has the AI Thinker ESP32-CAM and laptop. The shopping list below is a **small 3 V demonstration rig only**, not a production-module tester. Indicative online prices checked 26 September 2026; inventory, tax, and shipping vary. The listed sensor parts total about **₹1,311** before a local ruler and shipping. The optional arm is a separate ₹970 parts subtotal and requires an excluded servo power supply; buying everything will exceed ₹2,000 all-in.

| Item | Approx. price | Use |
|---|---:|---|
| ESP32-CAM-MB CH340G programmer (only if you do not already have an upload adapter) | ₹85 | USB programming; [Robo Bazar](https://robobazar.in/product/esp32-cam-mb-micro-usb-download-module-for-esp32-cam-development-board/) |
| INA219 breakout | ₹229 | Low-voltage bus/current telemetry; [Robu](https://robu.in/product/7semi-ina219-voltage-current-power-monitor-sensor-breakout-i2c-0-v-to-26-v/) |
| 0.45 W, 3 V mini solar panel | ₹156 | Safe, low-voltage bench source; [Robu](https://robu.in/product/0-45w-3v-150ma-mini-solar-panel-8x6-cm/) |
| Pro-Range SM-01 multimeter | ₹699 | Independent low-voltage voltage cross-check only; [Robu](https://robu.in/product/pro-range-sm-01-smart-digital-multimeter/) |
| Breadboard, 830-point | ₹61 | Temporary sensor wiring; [Robu](https://robu.in/product-category/electronic-components/breadboard-and-zero-pcb/) |
| Female-to-female and male-to-female jumper leads | ₹41 + ₹39 | I2C and breadboard connections; [Robu](https://robu.in/product-category/dupont-cable/) |
| 100 Ω, 0.25 W through-hole resistor | about ₹1-10 | Small dummy load for a 3 V panel; [Robu resistor listings](https://robu.in/product-category/carbon-resistors/) |
| 15 cm steel ruler | roughly ₹30-100 locally | Measure the 80 × 60 mm demo module; enter dimensions manually. |

The INA219 adapter is enabled by default, expects address `0x41` (set the module A0 address pad), and only reports raw low-voltage readings with `not_tested`; it never asserts pass/fail. Record front and rear images under the same panel reference using `view=front`, then `view=rear_nameplate` or `view=rear_junction_box`. The EYE app labels and appends each image to the same passport. See the [build guide](docs/STAGE1_SORTER_BUILD.md) for the optional acrylic arm parts and its calibration boundary.

The INA219 chip has a 26 V common-mode limit and the breakout calibration is set to 16 V/400 mA; the adapter reports raw readings and always transmits `not_tested`. It does not calculate pass/fail. The sketch depends on **Adafruit INA219** from Arduino Library Manager (installed on this PC); the adapter is enabled by default and reports “not detected” if the sensor is absent. It expects INA219 I²C address `0x41` so a future PCA9685 arm driver can use its common default `0x40`. Set the INA219 breakout's A0 address jumper to `0x41` before connecting; if your board has no address jumper, do not share its bus with the PCA9685. Connect the sensor to the ESP32-CAM at 3.3 V, SDA GPIO13, SCL GPIO14, and common GND; those pins are shared with the microSD interface, so do not use microSD while the sensor is connected. In series on the mini-panel side, wire panel `+` to INA219 `VIN+`, INA219 `VIN-` to the resistor, and the resistor to panel `-`; connect sensor and ESP32 grounds to panel `-`.

**Do not connect a full-size panel or string to this cheap breakout, breadboard, or ESP32.** PV open-circuit voltage and short-circuit current can exceed the module/board limits and create shock, arc, or fire hazards. Real-module electrical testing is a later stage requiring a correctly rated, isolated PV tester and a qualified operator. Even within this demo, verify polarity and wiring before exposing the panel to light.

## PC-only workflow test

```powershell
py tools/simulate_esp32.py
```

This uses a synthetic non-panel image, stub classifier, temporary database, and loopback HTTP server. It verifies authenticated uploads, retrieval and hash verification of the saved image URL, RGB/NIR modality handling, retries, safety routing, ordered Stage 2-4 measured events, and passport hash chains. It does not test real camera hardware, sensors, panel measurements, robot/PLC equipment, or model accuracy.

The [repair and hardware audit](docs/SYSTEM_REPAIR_AUDIT_2026-11-19.md) records the 19–20 November 2026 verification: 65/65 unit tests and the PC-only simulator passed in the launcher-selected Python 3.12 environment. The earlier partial Python 3.14 run, which lacked PyTorch, NumPy, and Pillow, remains documented in [the historical Stage 1 validation run](docs/STAGE1_VALIDATION_RUN_2026-11-19.md). The latest rerun and limits are in [the 20 November validation record](docs/STAGE1_VALIDATION_RUN_2026-11-20.md).

See [Stage 1 sorter build](docs/STAGE1_SORTER_BUILD.md) for the current order list, sensor wiring, rear-capture workflow, model/data limits, arm budget, and what must be calibrated before any physical sorting.

## Layout

```text
app.py                  Local operator app and versioned device API
firmware/agastya_eye/   AI Thinker ESP32-CAM sketch and optional INA219 adapter
firmware/servo_gate/    Optional Uno/Nano tabletop servo gate
inference/              CPU vision model loader, triage, and SQLite ledger
web/                    Operator interface
datasets/               Source notes, provenance, grouping, and training data
training/               Dataset import, split preparation, and model training
tools/                  PC-only device-protocol simulator
database/               Inspection ledger
images/                 Retained inspection photographs
```


