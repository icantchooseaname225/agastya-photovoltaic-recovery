"""Transparent inspection calculations and modality-gated research estimates."""

import json
import logging
import math
import threading
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOGGER = logging.getLogger(__name__)
MODEL_MODALITIES = {
    "near_infrared": "BW",
    "electroluminescence": "EL",
}


def supported_power_loss_model(camera_modality):
    return MODEL_MODALITIES.get(str(camera_modality or "").lower())


def calculate_panel_estimates(width_mm, height_mm, voltage, current, power, rated_power_w):
    area = None
    if width_mm is not None and height_mm is not None:
        area = round(float(width_mm) * float(height_mm) / 1_000_000, 4)

    if power is not None:
        power_w = round(float(power), 3)
        power_source = "recorded"
    elif voltage is not None and current is not None:
        power_w = round(float(voltage) * float(current), 3)
        power_source = "voltage_current_product"
    else:
        power_w = None
        power_source = None

    nameplate_pct = None
    below_nameplate_pct = None
    if power_w is not None and rated_power_w is not None and float(rated_power_w) > 0:
        nameplate_pct = round(100 * power_w / float(rated_power_w), 1)
        below_nameplate_pct = round(max(0.0, 100.0 - nameplate_pct), 1)

    return {
        "panel_area_m2": area,
        "power_w": power_w,
        "power_source": power_source,
        "nameplate_output_pct": nameplate_pct,
        "below_nameplate_pct": below_nameplate_pct,
        "interpretation": (
            "Area uses outer frame dimensions. Nameplate comparison is an uncorrected snapshot, "
            "not a standardized performance test or degradation diagnosis."
        ),
    }


class ResearchPowerLossEstimator:
    """Loads existing CC BY benchmark artifacts lazily for NIR or EL inputs only."""

    def __init__(self, root=ROOT):
        self.root = Path(root)
        self._lock = threading.RLock()
        self._backbone = None
        self._torch = None
        self._preprocess = None
        self._artifacts = {}

    def estimate(self, image, camera_modality):
        model_modality = supported_power_loss_model(camera_modality)
        if model_modality is None:
            return {
                "status": "not_available",
                "estimated_power_loss_pct": None,
                "reason": "No matching image power-loss model for this camera modality.",
                "sorting_use": False,
            }
        try:
            with self._lock:
                model_weights, metadata, report = self._load_artifact(model_modality)
                features = self._extract_features(image)
                estimate = float(model_weights["intercept"] + features @ model_weights["coefficients"])
            from training.pv_degradation import power_loss_band

            estimate = min(100.0, max(0.0, estimate))
            metrics = report.get("overall_cell_held_out_metrics", {})
            return {
                "status": "research_only",
                "model_modality": model_modality,
                "estimated_power_loss_pct": round(estimate, 1),
                "benchmark_band": power_loss_band(estimate),
                "training_samples": metadata.get("training_samples"),
                "training_cells": metadata.get("training_cells", []),
                "held_out_mae_pct_points": metrics.get("mae_pct_points"),
                "source_doi": metadata.get("source_doi"),
                "source_license": metadata.get("source_license"),
                "sorting_use": False,
                "warning": (
                    "Exploratory estimate from 84 close-up images of two laboratory cells; "
                    "not validated for full panels, field conditions, or this camera. Never use for sorting."
                ),
            }
        except Exception:
            LOGGER.exception("Research power-loss estimate failed for %s", model_modality)
            return {
                "status": "unavailable",
                "estimated_power_loss_pct": None,
                "reason": "Research model or MobileNetV2 weights are unavailable; no estimate was produced.",
                "sorting_use": False,
            }

    def _load_artifact(self, modality):
        if modality in self._artifacts:
            return self._artifacts[modality]
        import numpy as np

        stem = f"pv_{modality.lower()}_power_loss_ridge_research"
        model_path = self.root / "models" / f"{stem}.npz"
        metadata_path = model_path.with_suffix(".json")
        if not model_path.is_file() or not metadata_path.is_file():
            raise FileNotFoundError("Research model artifact is missing")
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        if (metadata.get("status") != "exploratory_research_only_not_for_live_eye_triage"
                or metadata.get("modality") != modality):
            raise ValueError("Research model metadata does not match the requested modality")
        report_path = self.root / "datasets" / "processed" / "pv_degradation_benchmark" / f"{modality.lower()}_benchmark_report.json"
        report = json.loads(report_path.read_text(encoding="utf-8"))
        with np.load(model_path, allow_pickle=False) as saved:
            intercept = float(saved["intercept"])
            coefficients = saved["coefficients"].astype(np.float64)
        if coefficients.shape != (1280,) or not math.isfinite(intercept) or not np.isfinite(coefficients).all():
            raise ValueError("Research model artifact has invalid weights")
        self._artifacts[modality] = (
            {"intercept": intercept, "coefficients": coefficients}, metadata, report
        )
        return self._artifacts[modality]

    def _extract_features(self, image):
        import torch
        from torchvision import transforms
        from torchvision.models import MobileNet_V2_Weights, mobilenet_v2

        if self._backbone is None:
            torch.set_num_threads(min(4, torch.get_num_threads()))
            weights = MobileNet_V2_Weights.DEFAULT
            self._backbone = mobilenet_v2(weights=weights)
            self._backbone.classifier = torch.nn.Identity()
            self._backbone.eval()
            self._preprocess = transforms.Compose([
                transforms.Resize(256),
                transforms.CenterCrop(224),
                transforms.ToTensor(),
                transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
            ])
            self._torch = torch
        tensor = self._preprocess(image.convert("RGB")).unsqueeze(0)
        with self._torch.inference_mode():
            embedding = self._backbone.features(tensor)
            embedding = self._torch.nn.functional.adaptive_avg_pool2d(embedding, 1).flatten(1)
        return embedding.cpu().numpy().astype("float64")[0]
