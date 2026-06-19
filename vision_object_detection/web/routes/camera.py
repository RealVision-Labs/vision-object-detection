from __future__ import annotations

from fastapi import APIRouter

from vision_object_detection.web.dependencies import camera


router = APIRouter(prefix="/api", tags=["camera"])


@router.get("/status")
def status():
    return camera.status()


@router.post("/camera/start")
def start_camera():
    return camera.start()


@router.post("/camera/stop")
def stop_camera():
    return camera.stop()
