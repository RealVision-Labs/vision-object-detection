# Contributing

Thank you for helping build Vision Object Detection.

## Development Setup

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
```

## Guidelines

- Keep camera code inside `vision_object_detection/camera/`.
- Keep detection model code inside `vision_object_detection/detection/`.
- Keep web routes and UI inside `vision_object_detection/web/`.
- Do not commit large model files.
- Document model licenses before adding model download instructions.
