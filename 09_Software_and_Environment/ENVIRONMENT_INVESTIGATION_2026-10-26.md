# AGASTYA environment investigation

**Audit date:** 26 October 2026  
**Project:** C:\Agastya\Agastya-EYE  
**Purpose:** identify the interpreter and CUDA/PyTorch environment used by the application, then verify the model path without installing software or changing data.

## Finding

CUDA was available outside the project folder. The earlier launcher hardcoded one machine-specific Python 3.14 path, and the RGB, visible-crop and thermal model loaders explicitly placed models and input tensors on CPU. Python 3.14 already had compatible CUDA-enabled PyTorch and torchvision. The repair reused that installation; no package or CUDA reinstall was needed.

## Interpreters and GPU stack

| Environment | Interpreter and package versions | CUDA result |
|---|---|---|
| EYE-selected Python | Python 3.14.9; PyTorch 2.14.1+cu126; torchvision 0.29.1+cu126 | torch.version.cuda=12.6; CUDA initialized; RTX 4050 visible |
| Additional Python | Python 3.15.1; PyTorch 2.14.1+cu132 | torch.version.cuda=13.2; CUDA initialized; RTX 4050 visible |
| NVIDIA system | RTX 4050 Laptop GPU, driver 617.42, 6141 MiB; CUDA toolkit 13.4.92 | Toolkit 13.4 and PyTorch wheel runtimes coexist |

The CUDA toolkit version and a PyTorch wheel's runtime are different layers. The installed PyTorch wheels include their own CUDA runtime libraries. EYE uses the Python 3.14 cu126 build; the system CUDA 13.4 toolkit did not need to match that runtime.

## Commands and checks

- py -0p listed Python 3.14.9 and 3.15.1.
- nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv reported NVIDIA GeForce RTX 4050 Laptop GPU, driver 617.42 and 6141 MiB.
- nvcc --version reported CUDA compilation tools release 13.4, V13.4.92.
- Under Python 3.14, imports of torch, torchvision, NumPy and Pillow succeeded. torch.cuda.is_available() returned true; torch.version.cuda was 12.6; the GPU name query returned RTX 4050; a CUDA tensor matrix operation completed on cuda:0.
- Python 3.15 also imported its cu132 build and completed a CUDA tensor operation on cuda:0.
- The launcher probes candidate interpreters for Python 3.11+, Pillow, NumPy, PyTorch and torchvision. It honors AGASTYA_EYE_PYTHON, then a project .venv, py -3.14, py -3 and PATH Python. It prints the selected interpreter and package/device versions.

## Model and application result

All three available vision checkpoints (RGB, visible-crop and thermal) loaded and ran inference under Python 3.14 on cuda:0 (NVIDIA GeForce RTX 4050 Laptop GPU). This verifies local loading and a real inference path. It does not reproduce the RGB sidecar's 84.62% accuracy or 83.53% macro-F1 and does not establish performance on field panels.

The launcher restarted EYE at http://127.0.0.1:8765. The health endpoint reported all three models ready on CUDA. See the software repair report for test and API evidence.

## Limits

This result applies to this Windows laptop and installed driver. It does not establish that another computer has the same environment, that the model is accurate on independently sourced panels, or that camera, sensor, sorting and recycling hardware operate correctly. No package installation, weight update, dataset rewrite or database write was performed.
