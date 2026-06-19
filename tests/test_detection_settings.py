import numpy as np

from vision_object_detection.detection.base import Detection
from vision_object_detection.detection.settings import DetectionSettings


class StaticDetector:
    def __init__(self) -> None:
        self.confidence_threshold = 0.35

    def detect(self, frame):
        return [
            Detection("person", 0.9, 10, 10, 50, 50),
            Detection("person", 0.8, 80, 80, 120, 120),
            Detection("cup", 0.7, 400, 300, 450, 360),
        ]


def test_object_counts_group_by_label():
    settings = DetectionSettings()

    counts = settings.object_counts(
        [
            Detection("person", 0.9, 0, 0, 10, 10),
            Detection("cup", 0.8, 0, 0, 10, 10),
            Detection("person", 0.7, 0, 0, 10, 10),
        ]
    )

    assert counts == {"cup": 1, "person": 2}


def test_confidence_updates_detector_threshold():
    settings = DetectionSettings()
    detector = StaticDetector()

    settings.update_confidence(0.6)
    settings.detect(detector, np.zeros((480, 640, 3), dtype=np.uint8))

    assert detector.confidence_threshold == 0.6


def test_zone_filters_detections_by_box_center():
    settings = DetectionSettings()
    detector = StaticDetector()

    settings.update_zone(enabled=True, x1=0.0, y1=0.0, x2=0.25, y2=0.25)
    detections = settings.detect(detector, np.zeros((480, 640, 3), dtype=np.uint8))

    assert [detection.label for detection in detections] == ["person", "person"]
