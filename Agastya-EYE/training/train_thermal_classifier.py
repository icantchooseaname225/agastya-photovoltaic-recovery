"""Train an experimental thermal-only module classifier on RaptorMaps crops."""

import argparse
import csv
import hashlib
import json
import random
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import transforms
from torchvision.datasets import ImageFolder
from torchvision.models import MobileNet_V2_Weights, mobilenet_v2

ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = ROOT / "datasets" / "processed" / "thermal_infrared"
MODEL_PATH = ROOT / "models" / "solar_thermal_mobilenet_v2.pth"
IMAGE_SIZE = (80, 48)


def sha256_file(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_manifest(data_root):
    path = Path(data_root) / "thermal_manifest.csv"
    groups = {}
    counts = {split: 0 for split in ("train", "validation", "test")}
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        for row in csv.DictReader(file):
            split = row.get("split", "")
            group = row.get("group_id", "")
            relative = Path(row.get("relative_path", ""))
            if split not in counts or not group or relative.is_absolute() or ".." in relative.parts:
                raise ValueError("thermal manifest has an invalid split, group, or image path")
            previous = groups.setdefault(group, split)
            if previous != split:
                raise ValueError(f"exact-image group {group} crosses dataset splits")
            if not (Path(data_root) / relative).is_file():
                raise ValueError(f"thermal manifest image is missing: {relative}")
            counts[split] += 1
    if any(count == 0 for count in counts.values()):
        raise ValueError("thermal dataset must contain train, validation, and test images")
    return len(groups), counts


def make_loaders(batch_size, seed, data_root=DATA_ROOT):
    train_transform = transforms.Compose([
        transforms.Resize(IMAGE_SIZE),
        transforms.RandomHorizontalFlip(),
        transforms.RandomVerticalFlip(),
        transforms.RandomRotation(8),
        transforms.ColorJitter(brightness=0.08, contrast=0.12),
        transforms.ToTensor(),
        transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
    ])
    eval_transform = transforms.Compose([
        transforms.Resize(IMAGE_SIZE),
        transforms.ToTensor(),
        transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
    ])
    datasets = {
        "train": ImageFolder(Path(data_root) / "train", transform=train_transform),
        "validation": ImageFolder(Path(data_root) / "validation", transform=eval_transform),
        "test": ImageFolder(Path(data_root) / "test", transform=eval_transform),
    }
    classes = datasets["train"].classes
    if len(classes) < 2:
        raise ValueError("thermal training needs at least two classes")
    for split, dataset in datasets.items():
        if dataset.classes != classes:
            raise ValueError(f"{split} class folders differ from train")
        missing = [classes[i] for i, count in enumerate(np.bincount(dataset.targets, minlength=len(classes))) if not count]
        if missing:
            raise ValueError(f"{split} has no samples for: {', '.join(missing)}")
    generator = torch.Generator().manual_seed(seed)
    loaders = {
        "train": DataLoader(datasets["train"], batch_size=batch_size, shuffle=True, num_workers=0, generator=generator),
        "validation": DataLoader(datasets["validation"], batch_size=batch_size, shuffle=False, num_workers=0),
        "test": DataLoader(datasets["test"], batch_size=batch_size, shuffle=False, num_workers=0),
    }
    return loaders, classes


def evaluate(model, loader, criterion, device, class_count):
    model.eval()
    total_loss = 0.0
    total = 0
    confusion = np.zeros((class_count, class_count), dtype=np.int64)
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


def score_report(confusion, classes):
    per_class = {}
    f1_values = []
    for index, label in enumerate(classes):
        true_positive = int(confusion[index, index])
        precision = true_positive / max(int(confusion[:, index].sum()), 1)
        recall = true_positive / max(int(confusion[index, :].sum()), 1)
        f1 = 2 * precision * recall / max(precision + recall, 1e-12)
        per_class[label] = {"precision": precision, "recall": recall, "f1": f1}
        f1_values.append(f1)
    total = int(confusion.sum())
    return {
        "accuracy": float(np.trace(confusion) / max(total, 1)),
        "macro_f1": float(np.mean(f1_values)),
        "per_class": per_class,
        "confusion_matrix": confusion.tolist(),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--epochs", type=int, default=6)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--learning-rate", type=float, default=0.001)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--threads", type=int, default=4, help="CPU threads for local training")
    parser.add_argument("--head-only", action="store_true")
    parser.add_argument("--no-pretrained", action="store_true")
    parser.add_argument("--data-root", type=Path, default=DATA_ROOT)
    parser.add_argument("--output", type=Path, default=MODEL_PATH)
    args = parser.parse_args()
    if args.epochs < 1 or args.batch_size < 1 or args.learning_rate <= 0 or args.threads < 1:
        parser.error("epochs, batch-size, learning rate, and threads must be positive")

    random.seed(args.seed)
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    torch.set_num_threads(args.threads)
    torch.set_num_interop_threads(1)
    data_root = args.data_root if args.data_root.is_absolute() else ROOT / args.data_root
    try:
        group_count, manifest_counts = validate_manifest(data_root)
        loaders, classes = make_loaders(args.batch_size, args.seed, data_root)
    except (FileNotFoundError, ValueError) as error:
        parser.error(f"Thermal dataset is not ready: {error}")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    weights = None if args.no_pretrained else MobileNet_V2_Weights.DEFAULT
    model = mobilenet_v2(weights=weights)
    for parameter in model.parameters():
        parameter.requires_grad = False
    tune_last = not args.head_only
    if tune_last:
        for parameter in model.features[-1].parameters():
            parameter.requires_grad = True
    model.classifier[1] = nn.Linear(model.last_channel, len(classes))
    model.to(device)

    train_counts = np.bincount(loaders["train"].dataset.targets, minlength=len(classes))
    class_weights = len(loaders["train"].dataset) / (len(classes) * train_counts)
    criterion = nn.CrossEntropyLoss(weight=torch.tensor(class_weights, dtype=torch.float32, device=device))
    parameter_groups = [{"params": list(model.classifier.parameters()), "lr": args.learning_rate}]
    last_block = [parameter for parameter in model.features[-1].parameters() if parameter.requires_grad]
    if last_block:
        parameter_groups.append({"params": last_block, "lr": args.learning_rate * 0.05})
    optimizer = torch.optim.AdamW(parameter_groups, weight_decay=1e-4)
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode="min", factor=0.5, patience=1)
    output_path = args.output if args.output.is_absolute() else ROOT / args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    best_validation_loss = float("inf")
    best_epoch = 0
    stale_epochs = 0
    epoch = 0

    for epoch in range(args.epochs):
        model.train()
        if tune_last:
            model.features[:-1].eval()
        else:
            model.features.eval()
        for images, targets in loaders["train"]:
            images, targets = images.to(device), targets.to(device)
            optimizer.zero_grad(set_to_none=True)
            loss = criterion(model(images), targets)
            loss.backward()
            optimizer.step()
        validation_loss, _ = evaluate(model, loaders["validation"], criterion, device, len(classes))
        scheduler.step(validation_loss)
        print(f"Epoch {epoch + 1}/{args.epochs}: validation loss {validation_loss:.4f}", flush=True)
        if validation_loss < best_validation_loss:
            best_validation_loss = validation_loss
            best_epoch = epoch + 1
            stale_epochs = 0
            temporary = output_path.with_suffix(output_path.suffix + ".tmp")
            torch.save({key: value.detach().cpu() for key, value in model.state_dict().items()}, temporary)
            temporary.replace(output_path)
        else:
            stale_epochs += 1
            if stale_epochs >= 3:
                print("Early stopping after validation loss stopped improving", flush=True)
                break

    model.load_state_dict(torch.load(output_path, map_location=device, weights_only=True))
    test_loss, test_confusion = evaluate(model, loaders["test"], criterion, device, len(classes))
    source_report = data_root / "import_report.json"
    import_report = json.loads(source_report.read_text(encoding="utf-8"))
    metadata = {
        "architecture": "mobilenet_v2",
        "classes": classes,
        "modality": "thermal_infrared",
        "input_size": list(IMAGE_SIZE),
        "pretrained_imagenet": not args.no_pretrained,
        "fine_tuned_last_block": tune_last,
        "seed": args.seed,
        "epochs_requested": args.epochs,
        "epochs_run": epoch + 1,
        "best_epoch": best_epoch,
        "batch_size": args.batch_size,
        "device": str(device),
        "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "validation_loss": best_validation_loss,
        "test_loss": test_loss,
        "test_metrics": score_report(test_confusion, classes),
        "group_count": group_count,
        "split_image_counts": manifest_counts,
        "split_manifest_sha256": sha256_file(data_root / "thermal_manifest.csv"),
        "import_report_sha256": sha256_file(source_report),
        "source_dataset": import_report,
        "required_attribution": "Copyright (c) 2020 Raptor Maps, Inc.; preserve the MIT license notice.",
        "split_method": import_report["split_method"],
        "research_only": True,
        "limitations": import_report["research_limitations"],
        "severity_estimation": False,
        "defect_localization": False,
    }
    metadata_path = output_path.with_suffix(".json")
    temporary_metadata = metadata_path.with_suffix(".tmp")
    temporary_metadata.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    temporary_metadata.replace(metadata_path)
    print(json.dumps({"test_loss": test_loss, **metadata["test_metrics"]}, indent=2))
    print(f"Saved research-only thermal model to {output_path}")


if __name__ == "__main__":
    main()
