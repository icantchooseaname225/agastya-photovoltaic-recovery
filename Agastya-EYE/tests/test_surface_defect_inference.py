import unittest

from inference.visible_crop_classifier import VisibleCropDefectClassifier, format_surface_predictions
from PIL import Image
from training.pv_surface_defects import CLASS_NAMES


class SurfaceDefectInferenceTests(unittest.TestCase):
    def test_predictions_are_tagged_advisory_and_sorted_by_score(self):
        probabilities = [0.2, 0.91, 0.4, 0.1, 0.8]
        thresholds = [0.5] * len(CLASS_NAMES)
        result = format_surface_predictions(probabilities, thresholds)
        self.assertEqual(result[0]["label"], "broken")
        self.assertEqual(result[1]["label"], "scratch")
        self.assertEqual(len(result), 2)
        self.assertTrue(all(item["confidence"] >= item["threshold"] for item in result))
        self.assertTrue(all(item["advisory_only"] for item in result))
        self.assertEqual({item["model"] for item in result}, {"pv_multi_defect_visible_crop_research"})

    def test_scores_below_validation_threshold_are_not_reported_as_hints(self):
        result = format_surface_predictions([0.2] * len(CLASS_NAMES), [0.5] * len(CLASS_NAMES))
        self.assertEqual(result, [])

    def test_wrong_number_of_scores_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "match the class count"):
            format_surface_predictions([0.5], [0.5])

    def test_only_square_closeups_are_supported(self):
        self.assertTrue(VisibleCropDefectClassifier.supports_input(Image.new("L", (600, 600), 128)))
        self.assertTrue(VisibleCropDefectClassifier.supports_input(Image.new("RGB", (600, 600), "red")))
        self.assertFalse(VisibleCropDefectClassifier.supports_input(Image.new("L", (640, 512), 128)))
        self.assertFalse(VisibleCropDefectClassifier.supports_input(Image.new("L", (600, 400), 128)))
        self.assertFalse(VisibleCropDefectClassifier.supports_input(Image.new("L", (400, 400), 128)))


if __name__ == "__main__":
    unittest.main()
