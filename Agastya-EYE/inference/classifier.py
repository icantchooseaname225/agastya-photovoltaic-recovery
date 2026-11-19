"""Loads an explicitly trained solar MobileNetV2 checkpoint when one exists."""

import json
import threading
from pathlib import Path

from .device import device_status, prepare_model_for_inference, run_inference

LABELS = ("clean", "dust", "crack", "broken", "burned", "snow", "bird_drop", "other")
MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "solar_mobilenet_v2.pth"
METADATA_PATH = MODEL_PATH.with_suffix(".json")


class SolarClassifier:
    def __init__(self):
        self._lock = threading.RLock()
        self._model = None
        self._torch = None
        self._classes = []
        self._mtime = None
        self._error = None
        self._metadata = {}
        self._loading = False
        self._device = None
        self._device_note = None

    def status(self, *, load=True):
        if load:
            with self._lock:
                self._load_if_changed()

        model_mtime = MODEL_PATH.stat().st_mtime_ns if MODEL_PATH.is_file() else None
        loaded = self._model is not None and model_mtime == self._mtime
        if not MODEL_PATH.is_file():
            return {"ready": False, "loaded": False, "loading": False,
                    "message": "No solar-trained checkpoint installed", "classes": list(LABELS)}
        if self._error and self._mtime == model_mtime:
            return {"ready": False, "loaded": False, "loading": False,
                    "message": self._error, "classes": list(LABELS)}

        try:
            if not METADATA_PATH.is_file():
                raise ValueError("Model metadata is missing; train with the Agastya-EYE pipeline")
            with METADATA_PATH.open("r", encoding="utf-8") as file:
                metadata = json.load(file)
            classes = metadata.get("classes")
            if (not isinstance(classes, list) or len(classes) < 2
                    or len(classes) != len(set(classes)) or set(classes) - set(LABELS)):
                raise ValueError("Checkpoint classes must be a unique Agastya-EYE class subset")
        except Exception as error:
            return {"ready": False, "loaded": False, "loading": False,
                    "message": f"{type(error).__name__}: {error}", "classes": list(LABELS)}

        metrics = metadata.get("test_metrics", {})
        result = {
            "ready": True,
            "loaded": loaded,
            "loading": self._loading and not loaded,
            "message": (
                "Experimental RGB screening model loaded; no RGB crack/burn detector or field severity estimate; human review required"
                if loaded else
                "Experimental RGB checkpoint present; it is loading in the background or will load on first inspection; human review required"
            ),
            "classes": classes,
            "evaluation": {
                "test_accuracy": metrics.get("accuracy"),
                "test_macro_f1": metrics.get("macro_f1"),
                "test_images": metadata.get("split_image_counts", {}).get("test"),
            },
        }
        result.update(device_status(self._torch, self._device, self._device_note))
        if loaded and result.get("device_label"):
            result["message"] += f" · inference device {result['device_label']}"
        if self._device_note:
            result["message"] += f" · {self._device_note}"
        return result

    def predict(self, image):
        with self._lock:
            self._load_if_changed()
            if self._model is None:
                return []

            import numpy as np

            image = image.convert("RGB")
            width, height = image.size
            scale = 256 / min(width, height)
            image = image.resize((round(width * scale), round(height * scale)))
            left = (image.width - 224) // 2
            top = (image.height - 224) // 2
            image = image.crop((left, top, left + 224, top + 224))
            pixels = np.asarray(image, dtype=np.float32) / 255.0
            tensor = self._torch.from_numpy(pixels).permute(2, 0, 1)
            mean = self._torch.tensor((0.485, 0.456, 0.406))[:, None, None]
            std = self._torch.tensor((0.229, 0.224, 0.225))[:, None, None]
            tensor = ((tensor - mean) / std).unsqueeze(0)
            probabilities_tensor, self._device, note = run_inference(
                self._model,
                tensor,
                self._torch,
                self._device,
                lambda model, batch: self._torch.softmax(model(batch)[0], dim=0),
            )
            if note:
                self._device_note = note
            probabilities = probabilities_tensor.tolist()
            order = sorted(range(len(probabilities)), key=probabilities.__getitem__, reverse=True)
            return [
                {"label": self._classes[index], "confidence": float(probabilities[index])}
                for index in order
            ]

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
                raise ValueError("Model metadata is missing; train with the Agastya-EYE pipeline")
            with METADATA_PATH.open("r", encoding="utf-8") as file:
                metadata = json.load(file)
            classes = metadata.get("classes")
            if (not isinstance(classes, list) or len(classes) < 2
                    or len(classes) != len(set(classes)) or set(classes) - set(LABELS)):
                raise ValueError("Checkpoint classes must be a unique Agastya-EYE class subset")

            import torch
            from torchvision.models import mobilenet_v2

            model = mobilenet_v2(weights=None)
            model.classifier[1] = torch.nn.Linear(model.last_channel, len(classes))
            state = torch.load(MODEL_PATH, map_location="cpu", weights_only=True)
            model.load_state_dict(state)
            device, device_note = prepare_model_for_inference(model, torch)
            model.eval()
            self._device = device
            self._device_note = device_note
            self._torch = torch
            self._classes = classes
            self._metadata = metadata
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
