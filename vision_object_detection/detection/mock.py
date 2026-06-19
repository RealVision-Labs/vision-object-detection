from __future__ import annotations

import numpy as np

from vision_object_detection.detection.base import Detection


class MockDetector:
    """A deterministic placeholder detector for UI and API development."""

    def detect(self, frame: np.ndarray) -> list[Detection]:
        if frame.size == 0:
            return []

        height, width = frame.shape[:2]
        box_width = width // 3
        box_height = height // 3
        x1 = (width - box_width) // 2
        y1 = (height - box_height) // 2
        return [
            Detection(
                label="object",
                confidence=0.75,
                x1=x1,
                y1=y1,
                x2=x1 + box_width,
                y2=y1 + box_height,
            )
        ]
