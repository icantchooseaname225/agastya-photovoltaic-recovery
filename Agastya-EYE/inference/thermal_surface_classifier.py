"""Compatibility import for the renamed visible-close-up research model."""

from inference.visible_crop_classifier import (
    VisibleCropDefectClassifier as ThermalSurfaceClassifier,
    format_surface_predictions,
)

__all__ = ["ThermalSurfaceClassifier", "format_surface_predictions"]
