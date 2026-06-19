from __future__ import annotations

from dataclasses import dataclass
import threading
import time

import cv2
import numpy as np


@dataclass(frozen=True)
class CameraStatus:
    running: bool
    message: str


class OpenCVCamera:
    def __init__(self, source: int = 0, width: int = 640, height: int = 480) -> None:
        self.source = source
        self.width = width
        self.height = height
        self._capture: cv2.VideoCapture | None = None
        self._running = False
        self._message = "Camera is stopped."
        self._latest_frame: np.ndarray | None = None
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._worker: threading.Thread | None = None

    def start(self) -> CameraStatus:
        if self._running:
            return self.status()

        capture = cv2.VideoCapture(self.source)
        capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        if not capture.isOpened():
            self._message = "Unable to open camera."
            return self.status()

        self._capture = capture
        self._running = True
        self._stop_event.clear()
        self._worker = threading.Thread(target=self._capture_loop, daemon=True)
        self._worker.start()
        self._message = "Camera is running."
        return self.status()

    def stop(self) -> CameraStatus:
        self._stop_event.set()
        worker = self._worker
        self._worker = None
        if worker is not None and worker.is_alive():
            worker.join(timeout=1.0)

        if self._capture is not None:
            self._capture.release()
        self._capture = None
        self._running = False
        with self._lock:
            self._latest_frame = None
        self._message = "Camera is stopped."
        return self.status()

    def status(self) -> CameraStatus:
        return CameraStatus(running=self._running, message=self._message)

    def get_frame(self) -> np.ndarray | None:
        with self._lock:
            if self._latest_frame is None:
                return None
            return self._latest_frame.copy()

    def _capture_loop(self) -> None:
        while not self._stop_event.is_set():
            if self._capture is None:
                break
            ok, frame = self._capture.read()
            if not ok:
                self._message = "Camera is running, but no frame is available."
                time.sleep(0.05)
                continue
            with self._lock:
                self._latest_frame = frame
            self._message = "Camera is running."
            time.sleep(1 / 30)
