"""Advisory screen for square RGB close-ups using grayscale-crop research data."""

import json
import threading
from pathlib import Path

from .device import device_status, prepare_model_for_inference, run_inference

from training.pv_surface_defects import CLASS_NAMES

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "models" / "solar_grayscale_crop_surface_defects_mobilenet_v2.pth"
METADATA_PATH = MODEL_PATH.with_suffix(".json")
MODEL_ID = "pv_multi_defect_visible_crop_research"


def format_surface_predictions(probabilities, thresholds):
    if len(probabilities) != len(CLASS_NAMES) or len(thresholds) != len(CLASS_NAMES):
        raise ValueError("probabilities and thresholds must match the class count")
    return [
        {
            "label": CLASS_NAMES[index],
            "confidence": float(probabilities[index]),
            "threshold": float(thresholds[index]),
            "model": MODEL_ID,
            "advisory_only": True,
        }
        for index in sorted(range(len(CLASS_NAMES)), key=lambda item: probabilities[item], reverse=True)
        if float(probabilities[index]) >= float(thresholds[index])
    ]


class VisibleCropDefectClassifier:
    def __init__(self):
        self._lock = threading.RLock()
        self._model = None
        self._torch = None
        self._transform = None
        self._metadata = {}
        self._mtime = None
        self._error = None
        self._loading = False
        self._device = None
        self._device_note = None

    @staticmethod
    def supports_input(image):
        width, height = image.size
        return min(width, height) >= 512 and abs(width / max(height, 1) - 1.0) <= 0.08

    def status(self, *, load=True):
        if load:
            with self._lock:
                self._load_if_changed()

        model_mtime = MODEL_PATH.stat().st_mtime_ns if MODEL_PATH.is_file() else None
        loaded = self._model is not None and model_mtime == self._mtime
        if not MODEL_PATH.is_file():
            message = "No visible close-up research checkpoint installed"
            return {
                "ready": False, "loaded": False, "loading": False,
                "message": message, "classes": list(CLASS_NAMES),
                "research_only": True, "used_for_routing": False,
            }
        if self._error and self._mtime == model_mtime:
            return {
                "ready": False, "loaded": False, "loading": False,
                "message": self._error, "classes": list(CLASS_NAMES),
                "research_only": True, "used_for_routing": False,
            }

        try:
            if not METADATA_PATH.is_file():
                raise ValueError("visible close-up model metadata is missing")
            metadata = json.loads(METADATA_PATH.read_text(encoding="utf-8"))
            if (metadata.get("architecture") != "mobilenet_v2_multilabel"
                    or metadata.get("task") != "visible_rgb_closeup_image_level_multilabel_screening_from_boxes"
                    or metadata.get("modality") != "visible_rgb_closeup"
                    or metadata.get("classes") != list(CLASS_NAMES)
                    or not metadata.get("research_only")
                    or metadata.get("localization") is not False
                    or metadata.get("severity_estimation") is not False):
                raise ValueError("metadata does not match the visible-close-up research model contract")
            thresholds = metadata.get("validation_thresholds")
            if not isinstance(thresholds, list) or len(thresholds) != len(CLASS_NAMES):
                raise ValueError("visible close-up validation thresholds are missing")
        except Exception as error:
            return {
                "ready": False, "loaded": False, "loading": False,
                "message": f"{type(error).__name__}: {error}", "classes": list(CLASS_NAMES),
                "research_only": True, "used_for_routing": False,
            }

        metrics = metadata.get("test_metrics", {}).get("test_metrics_validation_thresholds", {})
        broken = metrics.get("per_class", {}).get("broken")
        result = {
            "ready": True,
            "loaded": loaded,
            "loading": self._loading and not loaded,
            "message": (
                "RGB close-up screen loaded from grayscale crops; unspecified source sensor band; broken/scratch/hotspot hints only, no burn class, severity, localization, or sort authority"
                if loaded else
                "RGB close-up checkpoint present; it is loading in the background or will load for matching close-ups; research hints only, no sort authority"
            ),
            "classes": list(CLASS_NAMES),
            "evaluation": {
                "test_macro_f1": metrics.get("macro_f1"),
                "test_exact_match_accuracy": metrics.get("exact_match_accuracy"),
                "test_images": metadata.get("split_image_counts", {}).get("test"),
                "per_class": metrics.get("per_class", {}),
                "broken_precision": broken.get("precision") if broken else None,
            },
            "source_license_status": metadata.get("dataset", {}).get("source_license_status"),
            "research_only": True,
            "used_for_routing": False,
            **device_status(self._torch, self._device, self._device_note),
        }
        if loaded and result.get("device_label"):
            result["message"] += f" · inference device {result['device_label']}"
        if self._device_note:
            result["message"] += f" · {self._device_note}"
        return result

    def predict(self, image):
        with self._lock:
            self._load_if_changed()
            if self._model is None or not self.supports_input(image):
                return []
            tensor = self._transform(image.convert("L").convert("RGB")).unsqueeze(0)
            probabilities_tensor, self._device, note = run_inference(
                self._model,
                tensor,
                self._torch,
                self._device,
                lambda model, batch: self._torch.sigmoid(model(batch)[0]),
            )
            if note:
                self._device_note = note
            return format_surface_predictions(
                probabilities_tensor.tolist(), self._metadata["validation_thresholds"]
            )

    def _load_if_changed(self):
        if not MODEL_PATH.is_file():
            self._model = None
            self._mtime = None
            self._device = None
            self._device_note = None
            return
        mtime = MODEL_PATH.stat().st_mtime_ns
        if self._model is not None and mtime == self._mtime:
            return
        self._loading = True
        try:
            if not METADATA_PATH.is_file():
                raise ValueError("visible close-up model metadata is missing")
            metadata = json.loads(METADATA_PATH.read_text(encoding="utf-8"))
            if (metadata.get("architecture") != "mobilenet_v2_multilabel"
                    or metadata.get("task") != "visible_rgb_closeup_image_level_multilabel_screening_from_boxes"
                    or metadata.get("modality") != "visible_rgb_closeup"
                    or metadata.get("classes") != list(CLASS_NAMES)
                    or not metadata.get("research_only")
                    or metadata.get("localization") is not False
                    or metadata.get("severity_estimation") is not False):
                raise ValueError("metadata does not match the visible-close-up research model contract")
            thresholds = metadata.get("validation_thresholds")
            if not isinstance(thresholds, list) or len(thresholds) != len(CLASS_NAMES):
                raise ValueError("visible close-up validation thresholds are missing")

            import torch
            from torchvision import transforms
            from torchvision.models import mobilenet_v2

            model = mobilenet_v2(weights=None)
            model.classifier[1] = torch.nn.Linear(model.last_channel, len(CLASS_NAMES))
            model.load_state_dict(torch.load(MODEL_PATH, map_location="cpu", weights_only=True))
            device, device_note = prepare_model_for_inference(model, torch)
            model.eval()
            transform = transforms.Compose([
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
            ])
            self._torch = torch
            self._metadata = metadata
            self._device = device
            self._device_note = device_note
            self._transform = transform
            self._mtime = mtime
            self._model = model
            self._error = None
        except Exception as error:
            self._model = None
            self._mtime = mtime
            self._device = None
            self._device_note = None
            self._error = f"{type(error).__name__}: {error}"
        finally:
            self._loading = False
