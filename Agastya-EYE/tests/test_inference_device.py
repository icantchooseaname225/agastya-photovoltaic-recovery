import math
import os
import unittest
from unittest.mock import patch

import torch
from PIL import Image

from inference.classifier import MODEL_PATH, SolarClassifier
from inference.device import prepare_model_for_inference, run_inference


class InferenceDeviceTests(unittest.TestCase):
    def test_cpu_override_runs_on_cpu(self):
        model = torch.nn.Linear(2, 2)
        with patch.dict(os.environ, {"AGASTYA_EYE_DEVICE": "cpu"}):
            device, note = prepare_model_for_inference(model, torch)
            output, actual_device, fallback_note = run_inference(
                model, torch.ones(1, 2), torch, device, lambda network, batch: network(batch)
            )
        self.assertEqual(device.type, "cpu")
        self.assertEqual(actual_device.type, "cpu")
        self.assertEqual(output.device.type, "cpu")
        self.assertIn("CPU selected", note)
        self.assertIsNone(fallback_note)

    def test_auto_retries_cpu_after_cuda_forward_failure(self):
        model = torch.nn.Linear(2, 2)
        with patch.dict(os.environ, {"AGASTYA_EYE_DEVICE": "auto"}):
            output, device, note = run_inference(
                model,
                torch.ones(1, 2),
                torch,
                torch.device("cuda:0"),
                lambda network, batch: network(batch),
            )
        self.assertEqual(device.type, "cpu")
        self.assertEqual(output.device.type, "cpu")
        self.assertIn("CUDA inference failed", note)
        self.assertTrue(torch.isfinite(output).all().item())

    def test_invalid_device_setting_fails_with_actionable_error(self):
        model = torch.nn.Linear(2, 2)
        with patch.dict(os.environ, {"AGASTYA_EYE_DEVICE": "gpu-maybe"}):
            with self.assertRaisesRegex(ValueError, "AGASTYA_EYE_DEVICE"):
                prepare_model_for_inference(model, torch)

    @unittest.skipUnless(torch.cuda.is_available() and MODEL_PATH.is_file(), "CUDA or RGB checkpoint unavailable")
    def test_solar_checkpoint_prediction_uses_cuda(self):
        with patch.dict(os.environ, {"AGASTYA_EYE_DEVICE": "auto"}):
            classifier = SolarClassifier()
            status = classifier.status()
            predictions = classifier.predict(Image.new("RGB", (640, 480), "gray"))
        self.assertTrue(status["loaded"], status.get("message"))
        self.assertEqual(status["device"], "cuda:0")
        self.assertIn("NVIDIA GeForce RTX 4050", status["device_name"])
        self.assertTrue(predictions)
        self.assertAlmostEqual(sum(item["confidence"] for item in predictions), 1.0, places=5)
        self.assertTrue(all(math.isfinite(item["confidence"]) for item in predictions))


if __name__ == "__main__":
    unittest.main()
