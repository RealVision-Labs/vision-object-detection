# Vision Object Detection

Vision Object Detection is an open-source Python web app for general object detection. It is designed as the next RealVision Labs project after RealSense Toolkit.

The first version focuses on common object detection from a webcam or RealSense RGB stream. Depth integration can be added later as a separate milestone.

## Features

- Browser-based live detection dashboard
- General object detection pipeline
- OpenCV video capture support
- Detector abstraction for YOLO or future models
- FastAPI backend
- Modular frontend
- Repo-ready docs and tests

## Feature Status

| Feature | Status |
|---|---|
| Web dashboard | Starter |
| Webcam/RGB stream | Starter |
| Detection abstraction | Working |
| YOLO model loading | Working |
| Bounding box overlay | Starter |
| Screenshot/export | Planned |
| RealSense RGB support | Planned |
| Depth distance per object | Future project/milestone |

## Requirements

- Python 3.10+
- Webcam or RGB camera
- Windows, Linux, or macOS

## Installation

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

For development:

```powershell
pip install -r requirements-dev.txt
```

## Run

```powershell
uvicorn vision_object_detection.web.app:app --host 127.0.0.1 --port 8010
```

Open:

```text
http://127.0.0.1:8010
```

## YOLO Model

The app loads `yolo11n.pt` by default. You can change the detector without editing code:

```powershell
$env:VISION_MODEL="yolo11s.pt"
$env:VISION_CONFIDENCE="0.40"
$env:VISION_IMAGE_SIZE="640"
uvicorn vision_object_detection.web.app:app --host 127.0.0.1 --port 8010
```

Downloaded model files and local runtime settings are ignored by Git.

## Project Structure

```text
vision-object-detection/
  vision_object_detection/
    camera/
    detection/
    web/
  docs/
  tests/
```

## Roadmap

```text
v0.1.0 - Web dashboard and mock detector
v0.2.0 - YOLO detector
v0.3.0 - Detection overlays and snapshots
v0.4.0 - RealSense RGB input
v0.5.0 - Optional depth distance integration
```

## License

MIT License. See [LICENSE](LICENSE).
