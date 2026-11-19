"""PyTorch device selection with explicit, observable CPU fallback."""

import os

DEVICE_ENV = "AGASTYA_EYE_DEVICE"
VALID_DEVICE_PREFERENCES = {"auto", "cpu", "cuda"}


def device_preference():
    value = os.environ.get(DEVICE_ENV, "auto").strip().lower()
    if value not in VALID_DEVICE_PREFERENCES:
        choices = ", ".join(sorted(VALID_DEVICE_PREFERENCES))
        raise ValueError(f"{DEVICE_ENV} must be one of: {choices}")
    return value


def _error_text(error):
    return f"{type(error).__name__}: {error}"


def prepare_model_for_inference(model, torch):
    """Move a model to the requested device; auto mode falls back visibly."""
    preference = device_preference()
    cpu = torch.device("cpu")
    if preference == "cpu":
        model.to(cpu)
        return cpu, "CPU selected by AGASTYA_EYE_DEVICE."

    try:
        available = torch.cuda.is_available()
    except Exception as error:
        if preference == "cuda":
            raise RuntimeError(f"CUDA availability check failed: {_error_text(error)}") from error
        model.to(cpu)
        return cpu, f"CUDA check failed ({_error_text(error)}); CPU fallback active."

    if not available:
        if preference == "cuda":
            raise RuntimeError(
                f"{DEVICE_ENV}=cuda was requested, but torch.cuda.is_available() is false. "
                "Check the selected Python environment, CUDA-enabled PyTorch build, driver, and GPU visibility."
            )
        model.to(cpu)
        return cpu, "CUDA is unavailable to PyTorch; CPU fallback active."

    cuda = torch.device("cuda:0")
    try:
        model.to(cuda)
        torch.cuda.get_device_name(cuda)
        return cuda, None
    except Exception as error:
        if preference == "cuda":
            raise RuntimeError(f"CUDA model initialization failed: {_error_text(error)}") from error
        model.to(cpu)
        return cpu, f"CUDA initialization failed ({_error_text(error)}); CPU fallback active."


def run_inference(model, tensor, torch, device, operation):
    """Run one forward pass and retry on CPU only in auto mode after CUDA failure."""
    preference = device_preference()
    with torch.inference_mode():
        try:
            result = operation(model, tensor.to(device))
            return result.detach().cpu(), device, None
        except Exception as error:
            if device.type != "cuda" or preference != "auto":
                raise
            cpu = torch.device("cpu")
            try:
                model.to(cpu)
                result = operation(model, tensor.to(cpu))
                return (
                    result.detach().cpu(),
                    cpu,
                    f"CUDA inference failed ({_error_text(error)}); CPU fallback active.",
                )
            except Exception as fallback_error:
                raise RuntimeError(
                    f"CUDA inference failed ({_error_text(error)}) and CPU fallback failed "
                    f"({_error_text(fallback_error)})."
                ) from fallback_error


def device_status(torch, device, note=None):
    if device is None:
        return {"device": None, "device_name": None, "device_note": note}
    name = None
    if device.type == "cuda":
        try:
            name = torch.cuda.get_device_name(device)
        except Exception as error:
            note = note or f"GPU name query failed ({_error_text(error)})."
    label = str(device) if name is None else f"{device} ({name})"
    return {
        "device": str(device),
        "device_name": name,
        "device_label": label,
        "device_note": note,
    }
