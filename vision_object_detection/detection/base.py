from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

import numpy as np


@dataclass(frozen=True)
class Detection:
    label: str
    confidence: float
    x1: int
    y1: int
    x2: int
    y2: int


class ObjectDetector(Protocol):
    def detect(self, frame: np.ndarray) -> list[Detection]:
        ...
