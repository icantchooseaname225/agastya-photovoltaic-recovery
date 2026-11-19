"""Train a separate visible close-up multi-label screen from audited source boxes."""

import argparse
import hashlib
import json
import random
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import torch
from PIL import Image
from torch import nn
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
from torchvision.models import mobilenet_v2

from training.pv_surface_defects import CLASS_NAMES, labels_to_multihot, select_f1_thresholds

ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = ROOT / "datasets" / "processed" / "pv_multi_defect"
BASE_CHECKPOINT = ROOT / "models" / "solar_mobilenet_v2.pth"
MODEL_PATH = ROOT / "models" / "solar_grayscale_crop_surface_defects_mobilenet_v2.pth"
REPORT_PATH = MODEL_PATH.with_suffix(".json")


class SurfaceDefectDataset(Dataset):
    def __init__(self, split, transform):
        self.transform = transform
        manifest = DATA_ROOT / "annotations" / f"{split}.jsonl"
        self.rows = [json.loads(line) for line in manifest.read_text(encoding="utf-8").splitlines() if line]
        if not self.rows:
            raise ValueError(f"No image rows found in {manifest}")

    def __len__(self):
        return len(self.rows)

    def __getitem__(self, index):
        row = self.rows[index]
        image_path = DATA_ROOT / row["image"]
        with Image.open(image_path) as image:
            image = self.transform(image.convert("L").convert("RGB"))
        labels = {item["label"] for item in row["objects"]}
        target = torch.tensor(labels_to_multihot(labels), dtype=torch.float32)
        return image, target


def sha256_file(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_model():
    model = mobilenet_v2(weights=None)
    model.classifier[1] = nn.Linear(model.last_channel, len(CLASS_NAMES))
    base_state = torch.load(BASE_CHECKPOINT, map_location="cpu", weights_only=True)
    feature_state = {key: value for key, value in base_state.items() if key.startswith("features.")}
    missing, unexpected = model.load_state_dict(feature_state, strict=False)
    if unexpected or any(not key.startswith("classifier.") for key in missing):
        raise ValueError("The existing EYE RGB checkpoint does not match MobileNetV2 features")
    for parameter in model.features.parameters():
        parameter.requires_grad = False
    for parameter in model.features[-2:].parameters():
        parameter.requires_grad = True
    return model


def targets_for(dataset):
    rows = dataset.rows
    return np.asarray([
        labels_to_multihot({item["label"] for item in row["objects"]}) for row in rows
    ], dtype=np.float32)


def score_model(model, loader, criterion, device):
    model.eval()
    loss_sum = 0.0
    count = 0
    probabilities, targets = [], []
    with torch.inference_mode():
        for images, labels in loader:
            images, labels = images.to(device), labels.to(device)
            logits = model(images)
            loss_sum += criterion(logits, labels).item() * len(labels)
            count += len(labels)
            probabilities.extend(torch.sigmoid(logits).cpu().tolist())
            targets.extend(labels.cpu().tolist())
    return loss_sum / max(count, 1), probabilities, targets


def multilabel_report(probabilities, targets, thresholds):
    per_class = {}
    f1_values = []
    for class_index, label in enumerate(CLASS_NAMES):
        tp = fp = fn = 0
        for scores, actual in zip(probabilities, targets):
            predicted = scores[class_index] >= thresholds[class_index]
            expected = bool(actual[class_index])
            tp += predicted and expected
            fp += predicted and not expected
            fn += not predicted and expected
        precision = tp / max(tp + fp, 1)
        recall = tp / max(tp + fn, 1)
        f1 = 2 * precision * recall / max(precision + recall, 1e-12)
        per_class[label] = {"precision": precision, "recall": recall, "f1": f1}
        f1_values.append(f1)
    exact_match = sum(
        all((scores[i] >= thresholds[i]) == bool(actual[i]) for i in range(len(CLASS_NAMES)))
        for scores, actual in zip(probabilities, targets)
    ) / max(len(targets), 1)
    return {"macro_f1": float(np.mean(f1_values)), "exact_match_accuracy": exact_match, "per_class": per_class}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--epochs", type=int, default=12)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--patience", type=int, default=3)
    parser.add_argument("--threads", type=int, default=4)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    if args.epochs < 1 or args.batch_size < 1 or args.patience < 1:
        raise ValueError("epochs, batch size, and patience must be positive")
    if not BASE_CHECKPOINT.is_file():
        raise FileNotFoundError(f"EYE RGB transfer checkpoint is missing: {BASE_CHECKPOINT}")

    random.seed(args.seed)
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    torch.set_num_threads(max(1, args.threads))
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    train_transform = transforms.Compose([
        transforms.Resize(256),
        transforms.RandomResizedCrop(224, scale=(0.84, 1.0), ratio=(0.94, 1.06)),
        transforms.RandomHorizontalFlip(),
        transforms.RandomVerticalFlip(),
        transforms.RandomRotation(5),
        transforms.ColorJitter(brightness=0.08, contrast=0.12),
        transforms.ToTensor(),
        transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
    ])
    eval_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
    ])
    datasets = {
        "train": SurfaceDefectDataset("train", train_transform),
        "validation": SurfaceDefectDataset("validation", eval_transform),
        "test": SurfaceDefectDataset("test", eval_transform),
    }
    for name in ("train", "validation", "test"):
        if len({row["image_sha256"] for row in datasets[name].rows}) != len(datasets[name]):
            raise ValueError(f"{name} has duplicate image hashes")
    all_hashes = {
        name: {row["image_sha256"] for row in dataset.rows}
        for name, dataset in datasets.items()
    }
    if (all_hashes["train"] & all_hashes["validation"]
            or all_hashes["train"] & all_hashes["test"]
            or all_hashes["validation"] & all_hashes["test"]):
        raise ValueError("identical image hashes cross the train/validation/test boundary")

    generator = torch.Generator().manual_seed(args.seed)
    loaders = {
        "train": DataLoader(datasets["train"], batch_size=args.batch_size, shuffle=True,
                            num_workers=0, generator=generator),
        "validation": DataLoader(datasets["validation"], batch_size=args.batch_size, shuffle=False, num_workers=0),
        "test": DataLoader(datasets["test"], batch_size=args.batch_size, shuffle=False, num_workers=0),
    }
    train_targets = targets_for(datasets["train"])
    positives = train_targets.sum(axis=0)
    pos_weight = np.clip((len(train_targets) - positives) / np.maximum(positives, 1), 1.0, 10.0)
    criterion = nn.BCEWithLogitsLoss(pos_weight=torch.tensor(pos_weight, dtype=torch.float32, device=device))
    model = build_model().to(device)
    optimizer = torch.optim.AdamW([
        {"params": model.features[-2:].parameters(), "lr": 0.00003},
        {"params": model.classifier.parameters(), "lr": 0.0003},
    ], weight_decay=0.0001)

    best_loss = float("inf")
    best_epoch = 0
    stale_epochs = 0
    for epoch in range(1, args.epochs + 1):
        model.train()
        train_loss = 0.0
        count = 0
        for images, labels in loaders["train"]:
            images, labels = images.to(device), labels.to(device)
            optimizer.zero_grad(set_to_none=True)
            loss = criterion(model(images), labels)
            loss.backward()
            optimizer.step()
            train_loss += loss.item() * len(labels)
            count += len(labels)
        validation_loss, _, _ = score_model(model, loaders["validation"], criterion, device)
        print(f"Epoch {epoch}/{args.epochs}: train loss {train_loss / max(count, 1):.4f}; validation loss {validation_loss:.4f}", flush=True)
        if validation_loss < best_loss:
            best_loss = validation_loss
            best_epoch = epoch
            stale_epochs = 0
            temporary = MODEL_PATH.with_suffix(".tmp")
            torch.save({key: value.detach().cpu() for key, value in model.state_dict().items()}, temporary)
            temporary.replace(MODEL_PATH)
        else:
            stale_epochs += 1
            if stale_epochs >= args.patience:
                break

    state = torch.load(MODEL_PATH, map_location=device, weights_only=True)
    model.load_state_dict(state)
    val_loss, val_probs, val_targets = score_model(model, loaders["validation"], criterion, device)
    thresholds = select_f1_thresholds(val_probs, val_targets)
    test_loss, test_probs, test_targets = score_model(model, loaders["test"], criterion, device)
    report = {
        "test_loss": test_loss,
        "test_metrics_validation_thresholds": multilabel_report(test_probs, test_targets, thresholds),
        "test_metrics_fixed_0_5": multilabel_report(test_probs, test_targets, [0.5] * len(CLASS_NAMES)),
    }
    import_report = json.loads((DATA_ROOT / "import_report.json").read_text(encoding="utf-8"))
    metadata = {
        "architecture": "mobilenet_v2_multilabel",
        "classes": list(CLASS_NAMES),
        "modality": "visible_rgb_closeup",
        "task": "visible_rgb_closeup_image_level_multilabel_screening_from_boxes",
        "input_size": [224, 224],
        "source_model": str(BASE_CHECKPOINT.relative_to(ROOT)),
        "source_model_sha256": sha256_file(BASE_CHECKPOINT),
        "dataset": import_report,
        "source_modality_note": import_report.get("image_format_note"),
        "seed": args.seed,
        "device": str(device),
        "epochs_requested": args.epochs,
        "epochs_run": epoch,
        "best_epoch": best_epoch,
        "batch_size": args.batch_size,
        "validation_loss": val_loss,
        "validation_thresholds": thresholds,
        "test_metrics": report,
        "split_image_counts": {name: len(dataset) for name, dataset in datasets.items()},
        "research_only": True,
        "image_level_thresholds_are_not_safety_calibration": True,
        "localization": False,
        "severity_estimation": False,
        "electrical_measurement": False,
        "limitations": [
            "Model predicts image-level label presence; it does not use bbox coordinates to localize defects.",
            "Source labels do not contain crack or burned classes; hotspots are not burn diagnoses.",
            "Source sensor spectral band is unspecified; transfer to the RGB close-up input is unvalidated.",
            "Dataset-specific license is undeclared and requires permission before redistribution/publication.",
            "No physical panel/site IDs; test scores are not estimates of field performance.",
            "The image-level score is not electrical, thermal, severity, or reuse evidence.",
        ],
        "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    REPORT_PATH.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    print(json.dumps({"validation_loss": val_loss, **report}, indent=2))
    print(f"Saved research-only visible close-up model to {MODEL_PATH}")


if __name__ == "__main__":
    main()
