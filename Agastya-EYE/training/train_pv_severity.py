"""Train an exploratory, cell-held-out PV power-loss regression benchmark."""

import argparse
import csv
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import torch
from PIL import Image
from torchvision import transforms
from torchvision.models import MobileNet_V2_Weights, mobilenet_v2

ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = ROOT / "datasets" / "raw" / "pv_el_hdr_bw_v1"
DEFAULT_REPORT_DIR = ROOT / "datasets" / "processed" / "pv_degradation_benchmark"
MODEL_PATH = ROOT / "models" / "pv_hdr_power_loss_ridge_research.npz"
MODEL_METADATA = MODEL_PATH.with_suffix(".json")
MODALITY_CSV = {
    "HDR": DATA_ROOT / "data" / "ELPV_DATA_FULL.CSV",
    "BW": DATA_ROOT / "data" / "ELPV_DATA_FULL.CSV",
    "EL": DATA_ROOT / "data" / "ELPV_DATA_FULL.CSV",
}

from pv_degradation import (  # noqa: E402
    fit_ridge,
    grouped_leave_one_cell_out,
    predict_ridge,
    power_loss_band,
    read_samples,
    regression_metrics,
)


def extract_features(samples, modality, batch_size=8):
    weights = MobileNet_V2_Weights.DEFAULT
    model = mobilenet_v2(weights=weights)
    model.classifier = torch.nn.Identity()
    model.eval()
    model.to(torch.device("cpu"))
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
    ])

    features = []
    with torch.inference_mode():
        for start in range(0, len(samples), batch_size):
            images = []
            for sample in samples[start:start + batch_size]:
                with Image.open(sample.image_path) as image:
                    images.append(preprocess(image.convert("RGB")))
            batch = torch.stack(images)
            embeddings = model.features(batch)
            embeddings = torch.nn.functional.adaptive_avg_pool2d(embeddings, 1).flatten(1)
            features.extend(embeddings.cpu().numpy())
    return np.asarray(features, dtype=np.float64), weights.url


def rank_counts(samples):
    labels = [sample.visible_damage.lower() for sample in samples]
    return {
        "samples_with_crack_word_in_visible_annotation": sum(bool(re.search(r"\bcrack", label)) for label in labels),
        "samples_with_burn_soot_or_melting_word_in_visible_annotation": sum(
            bool(re.search(r"burn|soot|melt|fire", label)) for label in labels
        ),
        "samples_with_source_bbox": sum(sample.bbox is not None for sample in samples),
        "source_degradation_level_counts": dict(sorted(Counter(sample.source_grade for sample in samples).items())),
        "visible_damage_descriptor_counts": dict(sorted(Counter(sample.visible_damage for sample in samples).items())),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--modality", choices=("HDR", "BW", "EL"), default="HDR")
    parser.add_argument("--alpha", type=float, default=100.0,
                        help="Fixed ridge regularization; choose before evaluation, not from the held-out folds")
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--report-dir", type=Path, default=DEFAULT_REPORT_DIR)
    parser.add_argument("--model-output", type=Path, default=None)
    args = parser.parse_args()
    if not np.isfinite(args.alpha) or args.alpha <= 0 or args.batch_size < 1:
        parser.error("alpha and batch-size must be positive")

    data_csv = MODALITY_CSV[args.modality]
    image_root = DATA_ROOT / "images"
    try:
        samples = sorted(read_samples(data_csv, image_root, args.modality), key=lambda item: item.sample_id)
        folds = grouped_leave_one_cell_out(samples)
    except (OSError, ValueError) as error:
        parser.error(f"benchmark data is not ready: {error}. First run training/import_pv_degradation.py")

    torch.set_num_threads(min(4, torch.get_num_threads()))
    print(f"Extracting frozen MobileNetV2 features for {len(samples)} {args.modality} images on CPU...")
    features, backbone_weights_url = extract_features(samples, args.modality, args.batch_size)
    targets = np.asarray([sample.power_loss_pct for sample in samples], dtype=np.float64)
    positions = {sample.sample_id: index for index, sample in enumerate(samples)}
    fold_results = []
    prediction_rows = []
    all_actual = []
    all_predicted = []
    all_baseline = []

    for train_samples, test_samples in folds:
        train_groups = {sample.group_id for sample in train_samples}
        test_groups = {sample.group_id for sample in test_samples}
        if train_groups & test_groups:
            raise RuntimeError("physical-cell leakage detected in benchmark split")
        train_indices = np.asarray([positions[item.sample_id] for item in train_samples])
        test_indices = np.asarray([positions[item.sample_id] for item in test_samples])
        intercept, coefficients = fit_ridge(features[train_indices], targets[train_indices], args.alpha)
        predicted = np.clip(predict_ridge(features[test_indices], intercept, coefficients), 0, 100)
        actual = targets[test_indices]
        baseline = np.full_like(actual, float(targets[train_indices].mean()))
        fold_metric = regression_metrics(actual, predicted)
        fold_metric["held_out_cell"] = next(iter(test_groups))
        fold_metric["training_cells"] = sorted(train_groups)
        fold_metric["training_samples"] = int(len(train_indices))
        fold_metric["mean_predictor_mae_pct_points"] = regression_metrics(actual, baseline)["mae_pct_points"]
        fold_results.append(fold_metric)
        all_actual.extend(actual.tolist())
        all_predicted.extend(predicted.tolist())
        all_baseline.extend(baseline.tolist())
        for sample, measured, estimate in zip(test_samples, actual.tolist(), predicted.tolist()):
            prediction_rows.append({
                "sample_id": sample.sample_id,
                "physical_cell_group": sample.group_id,
                "modality": args.modality,
                "source_degradation_level": sample.source_grade,
                "visible_damage_descriptor": sample.visible_damage,
                "measured_power_loss_pct": measured,
                "predicted_power_loss_pct": estimate,
                "predicted_loss_band": power_loss_band(estimate, sample.damage_kind),
                "bbox_xyxy": json.dumps(sample.bbox, separators=(",", ":")) if sample.bbox else "",
                "fold_held_out_cell": sample.group_id,
            })

    report_dir = args.report_dir if args.report_dir.is_absolute() else ROOT / args.report_dir
    report_dir.mkdir(parents=True, exist_ok=True)
    overall = regression_metrics(all_actual, all_predicted)
    overall["mean_predictor_mae_pct_points"] = regression_metrics(all_actual, all_baseline)["mae_pct_points"]
    if overall["mean_predictor_mae_pct_points"]:
        overall["mae_reduction_vs_mean_predictor_pct"] = 100 * (
            1 - overall["mae_pct_points"] / overall["mean_predictor_mae_pct_points"]
        )
    else:
        overall["mae_reduction_vs_mean_predictor_pct"] = None

    source_metadata_path = DATA_ROOT / "agastya_import.json"
    source_metadata = json.loads(source_metadata_path.read_text(encoding="utf-8"))
    report = {
        "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "status": "exploratory_research_only_not_for_live_eye_triage",
        "task": "predict controlled-test measured power-output loss percentage from one image modality",
        "modality": args.modality,
        "samples": len(samples),
        "physical_cells": sorted({sample.group_id for sample in samples}),
        "split_method": "leave-one-physical-cell-out; no cell appears in both train and test within a fold",
        "fold_count": len(folds),
        "architecture": "frozen torchvision MobileNetV2 ImageNet embedding + dual-form ridge regression",
        "backbone_weights_url": backbone_weights_url,
        "ridge_alpha": args.alpha,
        "input_size": [224, 224],
        "source": {
            "name": source_metadata["source"],
            "version": source_metadata["version"],
            "doi": source_metadata["doi"],
            "license": source_metadata["license"],
            "archive_sha256": source_metadata["archive_sha256"],
            "citation": source_metadata["citation"],
        },
        "limitations": [
            "Only two physical polycrystalline cells; the two folds are not an independent field validation.",
            "Images are controlled close-up laboratory cell images, not AI Thinker ESP32-CAM full-panel captures.",
            "The labels are controlled halogen-lamp power-loss measurements; they are not ESP32/INA219 readings.",
            "No model for localization, crack-vs-burn classification, or RGB-IR fusion is trained by this baseline.",
            "Predicted loss bands describe benchmark targets only; never use them to authorize sorting or reuse.",
        ],
        "source_annotation_summary": rank_counts(samples),
        "overall_cell_held_out_metrics": overall,
        "folds": fold_results,
    }
    predictions_path = report_dir / f"{args.modality.lower()}_cell_held_out_predictions.csv"
    with predictions_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(prediction_rows[0]))
        writer.writeheader()
        writer.writerows(sorted(prediction_rows, key=lambda row: row["sample_id"]))
    report_path = report_dir / f"{args.modality.lower()}_benchmark_report.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    model_output = args.model_output or (
        MODEL_PATH if args.modality == "HDR" else MODEL_PATH.with_name(f"pv_{args.modality.lower()}_power_loss_ridge_research.npz")
    )
    model_output = model_output if model_output.is_absolute() else ROOT / model_output
    intercept, coefficients = fit_ridge(features, targets, args.alpha)
    model_output.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(model_output, intercept=np.asarray(intercept), coefficients=coefficients)
    metadata_path = model_output.with_suffix(".json")
    metadata_path.write_text(json.dumps({
        "status": report["status"],
        "modality": args.modality,
        "architecture": report["architecture"],
        "training_samples": len(samples),
        "training_cells": report["physical_cells"],
        "ridge_alpha": args.alpha,
        "input_size": [224, 224],
        "backbone_weights_url": backbone_weights_url,
        "source_doi": source_metadata["doi"],
        "source_license": source_metadata["license"],
        "evaluation_report": str(report_path),
        "warning": "Research benchmark artifact only; not integrated with live EYE triage or field images.",
    }, indent=2), encoding="utf-8")
    print(json.dumps({
        "overall_cell_held_out_metrics": overall,
        "folds": fold_results,
        "report": str(report_path),
        "predictions": str(predictions_path),
        "research_model": str(model_output),
    }, indent=2))


if __name__ == "__main__":
    main()
