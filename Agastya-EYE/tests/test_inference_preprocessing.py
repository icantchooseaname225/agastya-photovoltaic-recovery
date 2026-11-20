import unittest

from PIL import Image
from torchvision import transforms

from inference.preprocessing import rgb_evaluation_transform


class RGBPreprocessingTests(unittest.TestCase):
    def test_live_transform_matches_training_evaluation_transform(self):
        image = Image.new("RGB", (391, 287), color=(31, 117, 203))
        training_transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
        ])

        actual = rgb_evaluation_transform()(image)
        expected = training_transform(image)

        self.assertEqual(tuple(actual.shape), (3, 224, 224))
        self.assertTrue((actual == expected).all().item())
