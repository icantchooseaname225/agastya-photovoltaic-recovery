"""Research-only infrared classifier; never substitutes for calibrated measurements."""

import json
import threading
from pathlib import Path

from .device import device_status, prepare_model_for_inference, run_inference

MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "solar_thermal_mobilenet_v2.pth"
METADATA_PATH = MODEL_PATH.with_suffix(".json")
EXPECTED_CLASSES = {
    "cell", "cell_multi", "cracking", "diode", "diode_multi", "hot_spot",
    "hot_spot_multi", "no_anomaly", "offline_module", "shadowing", "soiling", "vegetation",
}


class ThermalClassifier:
    def __init__(self):
        self._lock = threading.RLock()
        self._model = None
        self._torch = None
        self._transform = None
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
            return {
                "ready": False, "loaded": False, "loading": False,
                "message": "No thermal-specific checkpoint installed; thermal images are archived without inference",
                "classes": [], "research_only": True,
            }
        if self._error and self._mtime == model_mtime:
            return {"ready": False, "loaded": False, "loading": False,
                    "message": self._error, "classes": [], "research_only": True}

        try:
            if not METADATA_PATH.is_file():
                raise ValueError("thermal checkpoint metadata is missing")
            metadata = json.loads(METADATA_PATH.read_text(encoding="utf-8"))
            classes = metadata.get("classes")
            if (metadata.get("modality") != "thermal_infrared"
                    or not isinstance(classes, list)
                    or set(classes) != EXPECTED_CLASSES
                    or len(classes) != len(EXPECTED_CLASSES)):
                raise ValueError("checkpoint metadata does not match the supported thermal class set")
        except Exception as error:
            return {"ready": False, "loaded": False, "loading": False,
                    "message": f"{type(error).__name__}: {error}", "classes": [], "research_only": True}

        test_images = metadata.get("split_image_counts", {}).get("test", 0)
        if isinstance(test_images, dict):
            test_images = sum(test_images.values())
        result = {
            "ready": True,
            "loaded": loaded,
            "loading": self._loading and not loaded,
            "message": (
                "Research thermal classifier loaded; grayscale 24:40 crops only; image-level source split; "
                "human review required; no severity or temperature estimate"
                if loaded else
                "Research thermal checkpoint present; it is loading in the background or will load for thermal inspection; human review required"
            ),
            "classes": classes,
            "evaluation": {
                "test_accuracy": metadata.get("test_metrics", {}).get("accuracy"),
                "test_macro_f1": metadata.get("test_metrics", {}).get("macro_f1"),
                "test_images": test_images,
            },
            "research_only": True,
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
            image = image.convert("RGB")
            tensor = self._transform(image).unsqueeze(0)
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

    @staticmethod
    def supports_input(image):
        width, height = image.size
        ratio = width / max(height, 1)
        if abs(ratio - (24 / 40)) > 0.12:
            return False
        import numpy as np

        sample = np.asarray(image.convert("RGB").resize((24, 40)), dtype=np.int16)
        chroma = (np.abs(sample[:, :, 0] - sample[:, :, 1]).mean()
                  + np.abs(sample[:, :, 1] - sample[:, :, 2]).mean()) / 2
        return chroma <= 2.0

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
                raise ValueError("thermal checkpoint metadata is missing")
            metadata = json.loads(METADATA_PATH.read_text(encoding="utf-8"))
            classes = metadata.get("classes")
            if (metadata.get("modality") != "thermal_infrared"
                    or not isinstance(classes, list)
                    or set(classes) != EXPECTED_CLASSES
                    or len(classes) != len(EXPECTED_CLASSES)):
                raise ValueError("checkpoint metadata does not match the supported thermal class set")

            import torch
            from torchvision import transforms
            from torchvision.models import mobilenet_v2

            model = mobilenet_v2(weights=None)
            model.classifier[1] = torch.nn.Linear(model.last_channel, len(classes))
            state = torch.load(MODEL_PATH, map_location="cpu", weights_only=True)
            model.load_state_dict(state)
            device, device_note = prepare_model_for_inference(model, torch)
            model.eval()
            transform = transforms.Compose([
                transforms.Resize((80, 48)),
                transforms.ToTensor(),
                transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
            ])
            self._classes = classes
            self._metadata = metadata
            self._device = device
            self._device_note = device_note
            self._torch = torch
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
