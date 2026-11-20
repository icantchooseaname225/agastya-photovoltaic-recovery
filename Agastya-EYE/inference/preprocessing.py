"""Image transforms shared by RGB training evaluation and live inference."""


def rgb_evaluation_transform():
    """Match the deterministic Resize/CenterCrop transform used by training eval."""
    from torchvision import transforms

    return transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
    ])
