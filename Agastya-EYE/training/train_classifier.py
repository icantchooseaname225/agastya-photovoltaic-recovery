"""Fine-tune MobileNetV2 on the normalized, provenance-tracked EYE image folders."""

import argparse
import csv
import hashlib
import json
import random
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision.datasets import ImageFolder
from torchvision.models import MobileNet_V2_Weights, mobilenet_v2
from torchvision import transforms

ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = ROOT / "datasets" / "processed"
MODEL_PATH = ROOT / "models" / "solar_mobilenet_v2.pth"
METADATA_PATH = MODEL_PATH.with_suffix(".json")
LABELS = ("clean", "dust", "crack", "broken", "burned", "snow", "bird_drop", "other")


def make_loaders(batch_size, seed):
    train_transform = transforms.Compose([
        transforms.Resize(256),
        transforms.RandomResizedCrop(224, scale=(0.82, 1.0), ratio=(0.90, 1.10)),
        transforms.RandomHorizontalFlip(),
        transforms.RandomVerticalFlip(),
        transforms.RandomRotation(8),
        transforms.ColorJitter(brightness=0.12, contrast=0.12, saturation=0.10, hue=0.015),
        transforms.ToTensor(),
        transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
    ])
    eval_transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
    ])
    datasets = {
        "train": ImageFolder(DATA_ROOT / "train", transform=train_transform),
        "validation": ImageFolder(DATA_ROOT / "validation", transform=eval_transform),
        "test": ImageFolder(DATA_ROOT / "test", transform=eval_transform),
    }
    active_classes = datasets["train"].classes
    if len(active_classes) < 2 or set(active_classes) - set(LABELS):
        raise ValueError("Training data must contain at least two Agastya-EYE classes")
    for split, dataset in datasets.items():
        if dataset.classes != active_classes:
            raise ValueError(f"{split} class folders differ from train: {dataset.classes} vs {active_classes}")
        counts = np.bincount(dataset.targets, minlength=len(active_classes))
        missing = [active_classes[index] for index, count in enumerate(counts) if not count]
        if missing:
            raise ValueError(f"{split} data has no images for: {', '.join(missing)}")
    generator = torch.Generator().manual_seed(seed)
    loaders = {
        "train": DataLoader(datasets["train"], batch_size=batch_size, shuffle=True, num_workers=0, generator=generator),
        "validation": DataLoader(datasets["validation"], batch_size=batch_size, shuffle=False, num_workers=0),
        "test": DataLoader(datasets["test"], batch_size=batch_size, shuffle=False, num_workers=0),
    }
    return loaders, active_classes


def evaluate(model, loader, criterion, device, classes):
    model.eval()
    total_loss = 0.0
    total = 0
    confusion = np.zeros((len(classes), len(classes)), dtype=np.int64)
    with torch.inference_mode():
        for images, targets in loader:
            images, targets = images.to(device), targets.to(device)
            logits = model(images)
            total_loss += criterion(logits, targets).item() * len(targets)
            predictions = logits.argmax(1)
            for actual, predicted in zip(targets.cpu().tolist(), predictions.cpu().tolist()):
                confusion[actual, predicted] += 1
            total += len(targets)
    return total_loss / max(total, 1), confusion


def metrics(confusion, classes):
    results = {}
    scores = []
    for index, label in enumerate(classes):
        true_positive = int(confusion[index, index])
        precision = true_positive / max(int(confusion[:, index].sum()), 1)
        recall = true_positive / max(int(confusion[index, :].sum()), 1)
        f1 = 2 * precision * recall / max(precision + recall, 1e-12)
        results[label] = {"precision": precision, "recall": recall, "f1": f1}
        scores.append(f1)
    total = int(confusion.sum())
    return {
        "accuracy": float(np.trace(confusion) / max(total, 1)),
        "macro_f1": float(np.mean(scores)),
        "per_class": results,
        "confusion_matrix": confusion.tolist(),
    }


def sha256_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_group_splits():
    manifest_path = DATA_ROOT / "processed_manifest.csv"
    groups = defaultdict(set)
    with manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
        for row in csv.DictReader(file):
            group_id = (row.get("group_id") or "").strip()
            split = (row.get("split") or "").strip()
            if group_id and split:
                groups[group_id].add(split)
    leaked = [group_id for group_id, splits in groups.items() if len(splits) > 1]
    if leaked:
        raise ValueError(f"{len(leaked)} image groups cross train/validation/test splits")
    return len(groups)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--epochs", type=int, default=30)
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--learning-rate", type=float, default=0.001)
    parser.add_argument("--backbone-learning-rate", type=float, default=0.00005)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--head-only", action="store_true", help="Freeze all MobileNetV2 feature blocks")
    parser.add_argument("--fine-tune-last-block", action="store_true", help="Compatibility flag; last-block fine-tuning is already the default")
    parser.add_argument("--no-pretrained", action="store_true", help="Do not download ImageNet pretrained weights")
    parser.add_argument("--output", type=Path, default=MODEL_PATH, help="Checkpoint destination; metadata is written beside it")
    args = parser.parse_args()
    if args.epochs < 1 or args.batch_size < 1 or args.learning_rate <= 0 or args.backbone_learning_rate <= 0:
        parser.error("epochs, batch-size, and learning rates must be positive")

    random.seed(args.seed)
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    try:
        loaders, classes = make_loaders(args.batch_size, args.seed)
        group_count = validate_group_splits()
    except (FileNotFoundError, ValueError) as error:
        parser.error(f"Dataset is not ready: {error}")

    weights = None if args.no_pretrained else MobileNet_V2_Weights.DEFAULT
    model = mobilenet_v2(weights=weights)
    for parameter in model.parameters():
        parameter.requires_grad = False
    fine_tune_last_block = not args.head_only or args.fine_tune_last_block
    if fine_tune_last_block:
        for parameter in model.features[-1].parameters():
            parameter.requires_grad = True
    model.classifier[1] = nn.Linear(model.last_channel, len(classes))
    model.to(device)

    train_counts = np.bincount(loaders["train"].dataset.targets, minlength=len(classes))
    class_weights = len(loaders["train"].dataset) / (len(classes) * train_counts)
    criterion = nn.CrossEntropyLoss(weight=torch.tensor(class_weights, dtype=torch.float32, device=device))
    head_parameters = list(model.classifier.parameters())
    backbone_parameters = [parameter for parameter in model.features[-1].parameters() if parameter.requires_grad]
    parameter_groups = [{"params": head_parameters, "lr": args.learning_rate}]
    if backbone_parameters:
        parameter_groups.append({"params": backbone_parameters, "lr": args.backbone_learning_rate})
    optimizer = torch.optim.AdamW(parameter_groups, weight_decay=1e-4)
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode="min", factor=0.5, patience=2)
    best_validation_loss = float("inf")
    best_epoch = 0
    epochs_without_improvement = 0
    output_path = args.output if args.output.is_absolute() else ROOT / args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    for epoch in range(args.epochs):
        model.train()
        if fine_tune_last_block:
            model.features[:-1].eval()
        else:
            model.features.eval()
        for images, targets in loaders["train"]:
            images, targets = images.to(device), targets.to(device)
            optimizer.zero_grad(set_to_none=True)
            loss = criterion(model(images), targets)
            loss.backward()
            optimizer.step()
        validation_loss, _ = evaluate(model, loaders["validation"], criterion, device, classes)
        scheduler.step(validation_loss)
        print(f"Epoch {epoch + 1}/{args.epochs}: validation loss {validation_loss:.4f}")
        if validation_loss < best_validation_loss:
            best_validation_loss = validation_loss
            best_epoch = epoch + 1
            epochs_without_improvement = 0
            temporary_path = output_path.with_suffix(output_path.suffix + ".tmp")
            torch.save({key: value.detach().cpu() for key, value in model.state_dict().items()}, temporary_path)
            temporary_path.replace(output_path)
        else:
            epochs_without_improvement += 1
            if epochs_without_improvement >= 7:
                print("Early stopping: validation loss did not improve for 7 epochs")
                break

    state = torch.load(output_path, map_location=device, weights_only=True)
    model.load_state_dict(state)
    test_loss, test_confusion = evaluate(model, loaders["test"], criterion, device, classes)
    report = metrics(test_confusion, classes)
    metadata = {
        "architecture": "mobilenet_v2",
        "classes": list(classes),
        "pretrained_imagenet": not args.no_pretrained,
        "fine_tuned_last_block": fine_tune_last_block,
        "max_epochs": args.epochs,
        "epochs_run": epoch + 1,
        "best_epoch": best_epoch,
        "batch_size": args.batch_size,
        "learning_rate": args.learning_rate,
        "backbone_learning_rate": args.backbone_learning_rate,
        "seed": args.seed,
        "device": str(device),
        "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "validation_loss": best_validation_loss,
        "test_loss": test_loss,
        "test_metrics": report,
        "group_count": group_count,
        "split_image_counts": {split: len(loader.dataset) for split, loader in loaders.items()},
        "source_manifest_sha256": sha256_file(ROOT / "datasets" / "processed" / "processed_manifest.csv"),
    }
    metadata_path = output_path.with_suffix(".json")
    temporary_metadata = metadata_path.with_suffix(".tmp")
    temporary_metadata.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    temporary_metadata.replace(metadata_path)
    print(json.dumps({"test_loss": test_loss, **report}, indent=2))
    print(f"Saved CPU-compatible model to {output_path}")


if __name__ == "__main__":
    main()
