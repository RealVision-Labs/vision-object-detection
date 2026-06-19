from __future__ import annotations

from dataclasses import asdict, dataclass
from threading import Lock

import numpy as np

from vision_object_detection.detection.base import Detection, ObjectDetector


@dataclass(frozen=True)
class DetectionZone:
    enabled: bool = False
    x1: float = 0.0
    y1: float = 0.0
    x2: float = 1.0
    y2: float = 1.0


class DetectionSettings:
    def __init__(self, confidence: float = 0.35) -> None:
        self._lock = Lock()
        self._confidence = self._clamp_confidence(confidence)
        self._zone = DetectionZone()

    @property
    def confidence(self) -> float:
        with self._lock:
            return self._confidence

    @property
    def zone(self) -> DetectionZone:
        with self._lock:
            return self._zone

    def snapshot(self) -> dict[str, object]:
        with self._lock:
            return {
                "confidence": self._confidence,
                "zone": asdict(self._zone),
            }

    def update_confidence(self, value: float) -> dict[str, object]:
        with self._lock:
            self._confidence = self._clamp_confidence(value)
        return self.snapshot()

    def update_zone(
        self,
        *,
        enabled: bool,
        x1: float = 0.0,
        y1: float = 0.0,
        x2: float = 1.0,
        y2: float = 1.0,
    ) -> dict[str, object]:
        left = self._clamp_unit(min(x1, x2))
        right = self._clamp_unit(max(x1, x2))
        top = self._clamp_unit(min(y1, y2))
        bottom = self._clamp_unit(max(y1, y2))
        if right - left < 0.01 or bottom - top < 0.01:
            enabled = False
            left, top, right, bottom = 0.0, 0.0, 1.0, 1.0

        with self._lock:
            self._zone = DetectionZone(enabled=enabled, x1=left, y1=top, x2=right, y2=bottom)
        return self.snapshot()

    def detect(self, detector: ObjectDetector, frame: np.ndarray) -> list[Detection]:
        self._apply_confidence(detector)
        detections = detector.detect(frame)
        return self._filter_zone(detections, frame.shape)

    def object_counts(self, detections: list[Detection]) -> dict[str, int]:
        counts: dict[str, int] = {}
        for detection in detections:
            counts[detection.label] = counts.get(detection.label, 0) + 1
        return dict(sorted(counts.items()))

    def _apply_confidence(self, detector: ObjectDetector) -> None:
        if hasattr(detector, "confidence_threshold"):
            setattr(detector, "confidence_threshold", self.confidence)

    def _filter_zone(self, detections: list[Detection], frame_shape: tuple[int, ...]) -> list[Detection]:
        zone = self.zone
        if not zone.enabled:
            return detections

        height, width = frame_shape[:2]
        left = zone.x1 * width
        right = zone.x2 * width
        top = zone.y1 * height
        bottom = zone.y2 * height

        filtered = []
        for detection in detections:
            center_x = (detection.x1 + detection.x2) / 2
            center_y = (detection.y1 + detection.y2) / 2
            if left <= center_x <= right and top <= center_y <= bottom:
                filtered.append(detection)
        return filtered

    @staticmethod
    def _clamp_confidence(value: float) -> float:
        return round(max(0.05, min(0.95, float(value))), 2)

    @staticmethod
    def _clamp_unit(value: float) -> float:
        return max(0.0, min(1.0, float(value)))
