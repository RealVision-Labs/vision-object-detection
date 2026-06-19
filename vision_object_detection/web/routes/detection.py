from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from vision_object_detection.web.dependencies import camera, detector, detector_bundle, settings


router = APIRouter(prefix="/api", tags=["detections"])


class ConfidenceRequest(BaseModel):
    confidence: float


class ZoneRequest(BaseModel):
    enabled: bool
    x1: float = 0.0
    y1: float = 0.0
    x2: float = 1.0
    y2: float = 1.0


@router.get("/detections")
def detections():
    frame = camera.get_frame()
    if frame is None:
        return JSONResponse({"message": "No camera frame available.", "detections": []}, status_code=503)

    results = settings.detect(detector, frame)
    return {
        "count": len(results),
        "object_counts": settings.object_counts(results),
        "detections": [detection.__dict__ for detection in results],
    }


@router.get("/detector/status")
def detector_status():
    return {
        "name": detector_bundle.name,
        "message": detector_bundle.message,
        "fallback": detector_bundle.fallback,
    }


@router.get("/settings")
def detection_settings():
    return settings.snapshot()


@router.post("/settings/confidence")
def update_confidence(payload: ConfidenceRequest):
    return settings.update_confidence(payload.confidence)


@router.post("/settings/zone")
def update_zone(payload: ZoneRequest):
    return settings.update_zone(
        enabled=payload.enabled,
        x1=payload.x1,
        y1=payload.y1,
        x2=payload.x2,
        y2=payload.y2,
    )
