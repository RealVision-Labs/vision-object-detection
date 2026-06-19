import numpy as np

from vision_object_detection.detection.mock import MockDetector


def test_mock_detector_returns_center_box():
    frame = np.zeros((480, 640, 3), dtype=np.uint8)

    detections = MockDetector().detect(frame)

    assert len(detections) == 1
    assert detections[0].label == "object"
    assert detections[0].confidence == 0.75
    assert detections[0].x1 < detections[0].x2
    assert detections[0].y1 < detections[0].y2
