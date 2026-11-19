# Agastya EYE and Later-Stage Interfaces

## Camera decision

Keep the existing AI Thinker ESP32-CAM as the Stage 1 visible-light capture node. It sends JPEGs to the laptop; the laptop remains responsible for MobileNet inference, triage, the panel passport, and operator review. The sketch identifies its feed as `visible_rgb` and sends a stable camera ID.

Do not treat an "IR LED" or an OV2640 camera without its IR-cut filter as a calibrated RGB-plus-IR camera. Removing the filter can make a camera respond to near-infrared, but IR then contaminates its visible color image. Espressif's [camera-driver sensor list](https://github.com/espressif/esp32-camera#esp32-camera-driver) documents color OV2640/OV5640 sensors and separate monochrome sensors; the specialized OmniVision [OV2736 RGB-IR sensor](https://www.ovt.com/products/ov2736/) is not in that list. OV2736 is a raw-output, chip-scale-package sensor with a 4x4 RGB-IR pixel pattern, not a drop-in camera module for the AI Thinker board. A compatible carrier, sensor driver, image processing, and optical calibration would still be needed.

For the current budget prototype, buy no new camera. If NIR becomes useful, add a separately identified NoIR/monochrome camera path and collect a paired visible/NIR capture with the same `capture_group_id`. The application stores `near_infrared` and `electroluminescence` images as separate records and skips the RGB model. The distinct `thermal_infrared` modality can run the laptop's experimental RaptorMaps classifier; its classes and limitations appear in the passport evidence. Exact high-confidence `cracking` output raises `SAFETY_HOLD`; other thermal classes remain human-review evidence. No modalities are fused, and near-IR/EL remain unmodeled until matching datasets and sensors exist.

Thermal IR is not the same as near-IR reflectance. EYE does not accept a thermal image as calibrated temperature data; the current research classifier was trained on normalized 24x40 grayscale crops. Later stations should send calibrated temperatures as numeric Stage 3 measurements with an instrument and calibration reference. Camera imagery never measures voltage or current; those readings come from an appropriately rated instrument and retain their own provenance. The Stage 2-4 event schema, passport identity, and safety boundary are unchanged by adding this model.

## Passport and event API

`panel_id` is the durable Agastya identity. Serial numbers and site tags belong in `external_ref`. A station must keep the same `panel_id` while appending its own records; it must not overwrite an EYE inspection or turn a visual class into a measured material result.

The JSON passport at `GET /api/v1/panels/<panel-id>/passport` is schema `1.4`. It includes Stage 1 inspections, camera modality/sensor/capture-group metadata, stage events, the inspection/image integrity result, and a separate event-chain integrity result. Inspection hashes created before schema `1.3` continue to be verified with their original hash fields.

Each inspection exposes `sort_recommendation` plus a derived `sort_lane_decision`. The latter is a dry-run LEFT (reuse candidate), RIGHT (isolated c-Si Stage 2 route), or HOLD result. `actuator_commanded` is always false. LEFT is not reuse approval, and HOLD includes uncertain, unsafe, incomplete, and licensed-handler cases. `final_sort_destination` follows a reviewed route override. These fields add no hardware dependency and are not a command protocol; a future PLC/robot adapter must independently validate panel identity, interlocks, guarding, and operator authorization.

Authenticated stations append events using `POST /api/v1/panels/<panel-id>/events` with the same private-LAN bearer token configured as `AGASTYA_DEVICE_TOKEN`:

```json
{
  "event_id": "stage2-station1-event-0001",
  "stage_code": "stage_2",
  "event_type": "process_completed",
  "station_id": "stage2-station1",
  "occurred_at": "2026-09-26T10:30:00Z",
  "operator_id": "operator-01",
  "instrument_id": "scale-01",
  "calibration_ref": "scale-calibration-2026-09",
  "measurements": [
    {"name": "input_mass", "value": 18.2, "unit": "kg"},
    {"name": "aluminum_frame_output", "value": 2.1, "unit": "kg"}
  ],
  "note": "Example schema only; replace values with actual measurements."
}
```

Supported stages are `stage_2`, `stage_3`, and `stage_4`; event types are `measurement`, `material_output`, `process_started`, `process_completed`, and `safety_hold`. Measurement units include `g`, `kg`, `C`, `V`, `A`, `W`, `J`, `Wh`, `kWh`, `s`, `min`, `mm`, `count`, `percent`, and `rpm`. Measurement, material-output, and completion events require instrument and calibration IDs. A completion requires a recorded mass. The supported rpm unit is generic and does not imply a selected Stage 4 machine; Stage 3 completion also requires a temperature in `C`. Every event carries a timezone-aware timestamp, station, operator, and retry-safe `event_id`.

The API enforces this hand-off sequence: Stage 2 requires the latest EYE record to route to `STAGE_2_CSI` with isolation confirmed; Stage 3 requires a Stage 2 `process_completed` event; Stage 4 requires a Stage 3 `process_completed` event. These are record-integrity and workflow checks, not functional-safety interlocks. The endpoint only accepts observations and measurements; it has no motor, heater, robot, or sorter command fields. Events are append-only and chained independently from image-inspection records.

## Current stage boundaries

- **Stage 1 / EYE:** photograph and identify the panel, record measured frame dimensions, junction-box location, electrical-test provenance, technology, route recommendation, and human disposition. Measurements may arrive from rated instruments, but must retain instrument and calibration provenance. Keep uncertain panels in review. Never infer voltage, chemistry, or recovered mass from an image.
- **Stage 2:** use a fixture and supervised de-framing/de-junctioning process. Append input and separated-stream measurements, including the instrument/calibration and operator. Keep material streams distinct; EYE's c-Si route is a hand-off recommendation, not a robot recipe or safety approval.
- **Stage 3:** develop the thermal-separation sequence in simulation and safe cold trials first. A future station records calibrated zone temperatures, mass flows, equipment/station identity, and actual process events. The EYE camera/API does not control heating.
- **Stage 4:** its purpose is silver removal/recovery, while method, feed preparation, and product form remain open. Record a route only after it is selected and record traceable feed/output masses, route-specific conditions, and suitable independent assay results. Sampling, assay, mass accounting, and uncertainty analysis validate all four stages; they do not define Stage 4. No ECS, electrostatic, or other route is assumed by this API.

For the eventual robot line, keep EYE as a laptop-hosted perception and passport service. A robot middleware such as ROS 2 can consume approved station jobs when those are designed; a dedicated PLC/safety controller must own emergency stops, guarding, isolation, and actuator interlocks. The ESP32-CAM is a camera/telemetry node, not the line's safety controller. The Stage event API is the data boundary only and is not a PLC interface.

## Verification boundary

`py tools/simulate_esp32.py` tests the HTTP protocol, modality handling, safety-routing gates, stage order, event retries, measurement validation, and passport hashes against a temporary database and synthetic image. It does not test a real camera, IR optics, voltage/current instrument, robot, PLC, thermal system, or separator. The RGB model remains experimental and uses one public image source; the separate thermal research classifier uses RaptorMaps crops. No NIR/EL classifier is trained.
