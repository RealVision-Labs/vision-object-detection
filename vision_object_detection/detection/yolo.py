from __future__ import annotations

import os
from pathlib import Path

import numpy as np

from vision_object_detection.detection.base import Detection


class YoloDetector:
    def __init__(
        self,
        model_name: str = "yolo11n.pt",
        confidence_threshold: float = 0.35,
        image_size: int = 640,
    ) -> None:
        config_dir = Path(os.getenv("VISION_ULTRALYTICS_CONFIG_DIR", ".local/ultralytics"))
        config_dir.mkdir(parents=True, exist_ok=True)
        os.environ.setdefault("YOLO_CONFIG_DIR", str(config_dir.resolve()))

        from ultralytics import YOLO

        self.model_name = model_name
        self.confidence_threshold = confidence_threshold
        self.image_size = image_size
        self.model = YOLO(model_name)

    @property
    def name(self) -> str:
        return f"YOLO ({Path(self.model_name).name})"

    def detect(self, frame: np.ndarray) -> list[Detection]:
        if frame.size == 0:
            return []

        results = self.model.predict(
            source=frame,
            imgsz=self.image_size,
            conf=self.confidence_threshold,
            verbose=False,
        )
        detections: list[Detection] = []
        if not results:
            return detections

        result = results[0]
        names = result.names
        for box in result.boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            class_id = int(box.cls[0].item())
            confidence = float(box.conf[0].item())
            detections.append(
                Detection(
                    label=str(names.get(class_id, class_id)),
                    confidence=confidence,
                    x1=int(x1),
                    y1=int(y1),
                    x2=int(x2),
                    y2=int(y2),
                )
            )
        return detections
