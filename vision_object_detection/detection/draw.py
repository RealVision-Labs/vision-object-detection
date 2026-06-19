from __future__ import annotations

import cv2
import numpy as np

from vision_object_detection.detection.base import Detection
from vision_object_detection.detection.settings import DetectionZone


def draw_detections(
    frame: np.ndarray,
    detections: list[Detection],
    zone: DetectionZone | None = None,
) -> np.ndarray:
    output = frame.copy()
    if zone and zone.enabled:
        height, width = output.shape[:2]
        top_left = (int(zone.x1 * width), int(zone.y1 * height))
        bottom_right = (int(zone.x2 * width), int(zone.y2 * height))
        cv2.rectangle(output, top_left, bottom_right, (61, 165, 255), 2)
        cv2.putText(
            output,
            "Detection zone",
            (top_left[0] + 8, max(20, top_left[1] + 24)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2,
            cv2.LINE_AA,
        )

    for detection in detections:
        cv2.rectangle(output, (detection.x1, detection.y1), (detection.x2, detection.y2), (65, 208, 137), 2)
        label = f"{detection.label} {detection.confidence:.2f}"
        cv2.putText(
            output,
            label,
            (detection.x1, max(20, detection.y1 - 8)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (255, 255, 255),
            2,
            cv2.LINE_AA,
        )
    return output
