# Architecture

The app is split into four boundaries:

```text
vision_object_detection/camera/     Camera capture adapters
vision_object_detection/detection/  Detection interfaces and model implementations
vision_object_detection/web/        FastAPI app, routes, templates, static UI
tests/                              Unit tests
```

The first version uses a mock detector so the UI and route contracts can be developed before adding model weights.
