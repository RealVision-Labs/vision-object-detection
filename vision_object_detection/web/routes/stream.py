from __future__ import annotations

import time

import cv2
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from vision_object_detection.detection.draw import draw_detections
from vision_object_detection.web.dependencies import camera, detector, settings


router = APIRouter(tags=["stream"])


def _jpeg_stream():
    while True:
        frame = camera.get_frame()
        if frame is None:
            if not camera.status().running:
                break
            time.sleep(0.05)
            continue

        detections = settings.detect(detector, frame)
        output = draw_detections(frame, detections, settings.zone)
        ok, buffer = cv2.imencode(".jpg", output)
        if not ok:
            continue
        yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + buffer.tobytes() + b"\r\n"
        time.sleep(1 / 30)


@router.get("/stream")
def stream():
    return StreamingResponse(_jpeg_stream(), media_type="multipart/x-mixed-replace; boundary=frame")
