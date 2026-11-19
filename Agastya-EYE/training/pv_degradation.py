"""Validated reader and group-aware evaluation helpers for the PV degradation benchmark."""

import csv
import math
import re
from dataclasses import dataclass
from pathlib import Path


REQUIRED_COLUMNS = {
    "images_set_name",
    "PV_cell_name",
    "Power_output_loss [%] [V*I]",
    "Degradation_level",
    "incremental_damage_kind",
    "incremental_damage_HDR_visible_type",
    "EL_file_name",
}
MODALITIES = {"HDR", "BW", "EL"}
SAFE_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,80}$")


@dataclass(frozen=True)
class PVSample:
    sample_id: str
    group_id: str
    image_path: Path
    modality: str
    power_loss_pct: float
    source_grade: str
    damage_kind: str
    visible_damage: str
    bbox: dict | None


def severity_band(power_loss_pct):
    """Map measured/predicted loss to the source paper's named damage bands."""
    loss = float(power_loss_pct)
    if not math.isfinite(loss) or not 0 <= loss <= 100:
        raise ValueError("power loss must be finite and between 0 and 100")
    if loss >= 100:
        return "catastrophic"
    if loss >= 45:
        return "critical"
    if loss >= 25:
        return "severe"
    if loss >= 15:
        return "moderate"
    if loss >= 5:
        return "minor"
    if loss > 0:
        return "light"
    return "none"


def power_loss_band(power_loss_pct, damage_kind=""):
    """Use the source's separate soiling thresholds for dirt rows."""
    loss = float(power_loss_pct)
    if not math.isfinite(loss) or not 0 <= loss <= 100:
        raise ValueError("power loss must be finite and between 0 and 100")
    if str(damage_kind).strip().lower() == "dirt":
        if loss >= 20:
            return "very_high_soiling"
        if loss >= 10:
            return "high_soiling"
        if loss >= 5:
            return "medium_soiling"
        return "low_soiling"
    return severity_band(loss)


def parse_bbox(row):
    fields = ("New_Damage_Xmin", "New_Damage_Ymin", "New_Damage_Xmax", "New_Damage_Ymax")
    raw = [(row.get(field) or "").strip() for field in fields]
    if not any(raw) or any(value.lower() in {"nan", "none", "null"} for value in raw):
        return None
    try:
        xmin, ymin, xmax, ymax = (int(value) for value in raw)
    except ValueError:
        return None
    if xmin < 0 or ymin < 0 or xmax <= xmin or ymax <= ymin:
        return None
    return {"xmin": xmin, "ymin": ymin, "xmax": xmax, "ymax": ymax}


def _image_path(row, image_root, modality):
    name = (row.get("images_set_name") or "").strip()
    if not SAFE_NAME.fullmatch(name) or ".." in name:
        raise ValueError(f"unsafe images_set_name: {name!r}")
    if modality == "HDR":
        filename = f"{name}_HDR_rt_cr.png"
    elif modality == "BW":
        filename = f"{name}_BN_rt_cr.png"
    else:
        filename = (row.get("EL_file_name") or "").strip()
        if not SAFE_NAME.fullmatch(filename) or Path(filename).name != filename:
            raise ValueError(f"unsafe EL filename for {name}")
    path = image_root / modality / filename
    if not path.is_file():
        raise ValueError(f"paired {modality} image is missing for {name}: {path}")
    return path


def read_samples(csv_path, image_root, modality="HDR"):
    modality = str(modality).upper()
    if modality not in MODALITIES:
        raise ValueError(f"modality must be one of {', '.join(sorted(MODALITIES))}")
    csv_path = Path(csv_path)
    image_root = Path(image_root)
    with csv_path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file, delimiter=";")
        missing = REQUIRED_COLUMNS - set(reader.fieldnames or ())
        if missing:
            raise ValueError(f"CSV is missing required columns: {', '.join(sorted(missing))}")
        rows = list(reader)

    samples = []
    seen = set()
    for row in rows:
        sample_id = (row.get("images_set_name") or "").strip()
        group_id = (row.get("PV_cell_name") or "").strip()
        if not SAFE_NAME.fullmatch(group_id):
            raise ValueError(f"invalid PV_cell_name for {sample_id!r}")
        if sample_id in seen:
            raise ValueError(f"duplicate sample id: {sample_id}")
        seen.add(sample_id)
        raw_loss = (row.get("Power_output_loss [%] [V*I]") or "").strip()
        try:
            loss = float(raw_loss)
        except ValueError as error:
            raise ValueError(f"{sample_id} has no finite power-loss measurement") from error
        if not math.isfinite(loss):
            raise ValueError(f"{sample_id} has no finite power-loss measurement")
        if not 0 <= loss <= 100:
            raise ValueError(f"{sample_id} power loss must be between 0 and 100")
        samples.append(PVSample(
            sample_id=sample_id,
            group_id=group_id,
            image_path=_image_path(row, image_root, modality),
            modality=modality,
            power_loss_pct=loss,
            source_grade=(row.get("Degradation_level") or "").strip(),
            damage_kind=(row.get("incremental_damage_kind") or "").strip(),
            visible_damage=(row.get("incremental_damage_HDR_visible_type") or "").strip(),
            bbox=parse_bbox(row),
        ))
    if not samples:
        raise ValueError("CSV contains no benchmark samples")
    return samples


def grouped_leave_one_cell_out(samples):
    """Return folds holding out every image from one physical cell at a time."""
    groups = sorted({sample.group_id for sample in samples})
    if len(groups) < 2:
        raise ValueError("at least two physical cells are required for grouped evaluation")
    folds = []
    for held_out in groups:
        train = [sample for sample in samples if sample.group_id != held_out]
        test = [sample for sample in samples if sample.group_id == held_out]
        if not train or not test:
            raise ValueError(f"cannot form a cell-held-out fold for {held_out}")
        folds.append((train, test))
    return folds


def fit_ridge(features, targets, alpha=100.0):
    """Fit a centered dual-form ridge regressor for small-sample image embeddings."""
    import numpy as np

    features = np.asarray(features, dtype=np.float64)
    targets = np.asarray(targets, dtype=np.float64)
    if features.ndim != 2 or targets.ndim != 1 or len(features) != len(targets) or not len(targets):
        raise ValueError("features must be a non-empty matrix aligned with one-dimensional targets")
    if not np.isfinite(features).all() or not np.isfinite(targets).all():
        raise ValueError("features and targets must be finite")
    if not math.isfinite(alpha) or alpha <= 0:
        raise ValueError("ridge alpha must be finite and positive")
    feature_mean = features.mean(axis=0)
    target_mean = targets.mean()
    centered_features = features - feature_mean
    gram = centered_features @ centered_features.T
    dual_weights = np.linalg.solve(gram + alpha * np.eye(len(targets)), targets - target_mean)
    weights = centered_features.T @ dual_weights
    intercept = float(target_mean - feature_mean @ weights)
    return intercept, weights


def predict_ridge(features, intercept, weights):
    import numpy as np

    features = np.asarray(features, dtype=np.float64)
    weights = np.asarray(weights, dtype=np.float64)
    if features.ndim != 2 or weights.ndim != 1 or features.shape[1] != len(weights):
        raise ValueError("feature columns must match ridge weights")
    return intercept + features @ weights


def regression_metrics(targets, predictions):
    import numpy as np

    targets = np.asarray(targets, dtype=np.float64)
    predictions = np.asarray(predictions, dtype=np.float64)
    if targets.ndim != 1 or targets.shape != predictions.shape or not len(targets):
        raise ValueError("targets and predictions must be non-empty vectors of the same shape")
    errors = predictions - targets
    variance = float(np.sum((targets - targets.mean()) ** 2))
    return {
        "n": int(len(targets)),
        "mae_pct_points": float(np.mean(np.abs(errors))),
        "rmse_pct_points": float(np.sqrt(np.mean(errors ** 2))),
        "r2": float(1.0 - np.sum(errors ** 2) / variance) if variance else None,
    }
