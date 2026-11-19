# Visible Close-Up Defect Screen

## Purpose

This MobileNetV2 multi-label screen accepts high-resolution square visible-camera close-ups. It is a separate research task from full-panel RGB screening, thermal imagery, EL, voltage/current tests, and sorting. Its predictions are attached as advisory evidence only; they do not change EYE's route or command an actuator.

## Data and target labels

Source: [PV-Multi-Defect](https://github.com/CCNUZFW/PV-Multi-Defect), pinned repository commit `2c4df0c1477032d6b0dd9372a517cdbfd6a09e09`. The originating [study](https://www.mdpi.com/2079-9292/12/3/561) describes camera images converted to grayscale and cropped, but does not specify the sensor's spectral band; later publications describe this dataset as infrared. Treat its modality as unverified grayscale camera crops, not calibrated thermal data or guaranteed RGB-equivalent data. The source box labels are `broken`, `hot_spot`, `black_border`, `scratch`, and `no_electricity`.

The audited import contains 1,108 source images; 60 exact-pixel duplicate groups with conflicting box annotations are excluded. The remaining rows are split 689/148/148 by image hash, not physical panel. Source images are close-up crops from a limited study, so repeated images from one panel may cross splits. This is not an independent-panel or field test.

The GitHub README cites a CC BY 3.0 paper, but does not declare a license for the separately hosted image files. Keep images and derived weights local until the dataset rights holder grants permission or a clear data license is documented. Do not redistribute this dataset or derived checkpoint on the basis of the paper license alone.

## Evaluation and limits

The fresh model's 148-image held-out split scored 70.0% macro-F1 and 58.8% exact-match accuracy at validation-selected thresholds. `broken` scored 62.5% precision, 45.5% recall, and 52.6% F1; `scratch` F1 was 88.0%. Full metrics are recorded in the ignored JSON report at `models/solar_grayscale_crop_surface_defects_mobilenet_v2.json` and displayed in EYE's Training Data page. Use the source annotation boxes only as labels in this baseline: the model does not predict locations, dimensions, or defect extent. Transfer from uncertain source optics to the RGB close-up input is unvalidated. The source has no `burned` label; `hot_spot` is not a burn diagnosis. The `no_electricity` image label is not an electrical measurement. There is no calibrated severity target, temperature, voltage/current, reuse outcome, or sorting label.

Predictions are unsuitable for standalone acceptance/rejection, safety decisions, or mechanical sorting. Verify every suspected defect physically and with separately calibrated electrical instruments. A weak metric must remain a warning, not a more aggressive confidence threshold.

## Reproduce

```powershell
py training/import_pv_multi_defect.py
py training/train_surface_defect_classifier.py --epochs 12 --batch-size 32 --threads 4
```

The importer preserves source annotations and conflict audits. The model uses an ImageNet/EYE MobileNetV2 feature initializer, image-level targets, validation-only threshold selection, and a held-out test report. Do not select thresholds or model versions by repeated tuning against the test split.
