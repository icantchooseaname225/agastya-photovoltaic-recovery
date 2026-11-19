# Thermal Model Card

## Purpose

This is a laptop-side research classifier for the `thermal_infrared` inspection modality. It is separate from the AI Thinker ESP32-CAM RGB stream and from the RGB MobileNetV2 checkpoint. Its output is a source class plus confidence, not a diagnosis, defect location, severity score, temperature, electrical test, or recycling decision.

## Dataset and labels

The model uses the RaptorMaps [InfraredSolarModules dataset](https://github.com/RaptorMaps/InfraredSolarModules), pinned at commit `88e2d1febbcefe401c17ec80b8973f36a02a1653`. The repository states the MIT License. The imported archive SHA-256 is `b82c706bc719b045ac4f8930570d81767a8a170d0998ca3e09283b585db05b5e`. Preserve the original attribution: Copyright (c) 2020 Raptor Maps, Inc. The source describes 20,000 24x40 grayscale infrared module crops.

The model retains all 12 original categories:

| Model label | Source meaning |
|---|---|
| `cell` | Hot spot with square geometry in one cell |
| `cell_multi` | Square hot spots across multiple cells |
| `cracking` | Module anomaly labeled as cracking |
| `diode` | One activated bypass diode, typically one third of a module |
| `diode_multi` | Multiple activated bypass diodes |
| `hot_spot` | Hot spot on a thin-film module |
| `hot_spot_multi` | Multiple thin-film hot spots |
| `no_anomaly` | Source-labeled nominal module |
| `offline_module` | Entire module is heated |
| `shadowing` | Partial obstruction/shading |
| `soiling` | Dirt, dust, or debris |
| `vegetation` | Vegetation blocking a panel |

There is no separate `burned` or `broken` class, no defect boxes/masks, and no measured severity target. EYE does not relabel hot spots or cracking as burns. These crops are not captured by the user's OV2640 camera; the RaptorMaps source is thermal imagery, not visible RGB or near-IR reflectance.

## Import and evaluation

`training/import_raptormaps_thermal.py` verifies the pinned archive hash, validates every image path and 24x40 image, preserves raw labels, computes content hashes, and writes source/version/license metadata. It found 22 repeated exact-image records and six image hashes assigned conflicting source labels (12 records). The conflicting groups remain in raw data and an audit CSV, but are omitted from training. Same-label duplicates are kept together and represented once in processed data, leaving 19,972 unique images.

The deterministic split is stratified by class and exact-image hash: approximately 70% train, 15% validation, and 15% test. The source provides no physical panel, array/site, or time identifiers. This split therefore prevents exact-pixel leakage only; it is **not panel-, site-, or time-independent validation**. Copies or neighboring crops from the same physical module may cross splits. The held-out metrics shown in the app are for research iteration only and must not be described as field performance.

The trainer fine-tunes the classifier head and final MobileNetV2 feature block, uses training-only spatial/brightness augmentation and class-weighted loss, early stopping on validation loss, and evaluates the test split once after selection. The matching inference transform resizes to 80x48 (height x width), a 2x scale of the source pixels that keeps aspect ratio, and uses ImageNet channel normalization. It accepts only grayscale crops with the source 24:40 aspect ratio; incompatible frames are archived without inference. Rebuild with:

```powershell
py training/import_raptormaps_thermal.py
py training/train_thermal_classifier.py --epochs 6 --batch-size 32
```

The CPU-compatible checkpoint is `models/solar_thermal_mobilenet_v2.pth`; metadata and per-class metrics are beside it. Dataset images and checkpoints are ignored by Git. Preserve the dataset attribution and license notice when retaining or distributing derived weights.

## EYE behavior

The inspection form and versioned device API accept `camera_modality: thermal_infrared`. Such images use only the thermal checkpoint. The panel passport stores the selected modality, sensor ID, capture group, predictions, and route evidence without changing the Stage 2-4 event schema. A high-confidence `cracking` result triggers `SAFETY_HOLD`; other thermal classes remain review-required. If no thermal checkpoint is installed, EYE archives the image and records that inference was skipped. No thermal result alone authorizes sorting, reuse, or destructive processing.

The AI Thinker ESP32-CAM still sends visible RGB only. EYE cannot manufacture a thermal channel from an RGB frame. A real thermal workflow needs a distinct sensor with calibration metadata and a separately paired capture ID. Normalized grayscale pixels are not absolute temperature; calibrated temperature and voltage/current remain instrument measurements.

## Gate before field use

Before any model affects operational sorting, collect and expert-review diverse whole-module thermal and RGB captures from multiple uniquely identified panels, sites, module technologies, seasons, and fault severities. Record sensor, optics, emissivity/temperature calibration, irradiance, environmental conditions, and paired qualified I-V results. Label panel-level defects and locations with a documented rubric; label severity from measured evidence rather than model confidence. Keep all views of a physical panel in one split, reserve a site/time-separated final test, report per-class recall and confusion (especially missed structural/electrical faults), and have qualified operators approve every outcome. Until that gate is met, this is a research aid, not a final-product sorter.
