from __future__ import annotations

from dataclasses import dataclass
import os

from vision_object_detection.detection.mock import MockDetector


@dataclass(frozen=True)
class DetectorBundle:
    detector: object
    name: str
    message: str
    fallback: bool


def create_detector() -> DetectorBundle:
    model_name = os.getenv("VISION_MODEL", "yolo11n.pt")
    confidence = float(os.getenv("VISION_CONFIDENCE", "0.35"))
    image_size = int(os.getenv("VISION_IMAGE_SIZE", "640"))

    try:
        from vision_object_detection.detection.yolo import YoloDetector

        detector = YoloDetector(
            model_name=model_name,
            confidence_threshold=confidence,
            image_size=image_size,
        )
        return DetectorBundle(
            detector=detector,
            name=detector.name,
            message="YOLO detector is active.",
            fallback=False,
        )
    except Exception as exc:
        return DetectorBundle(
            detector=MockDetector(),
            name="Mock detector",
            message=f"YOLO unavailable, using mock detector: {exc}",
            fallback=True,
        )
