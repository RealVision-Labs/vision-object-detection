from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles

from vision_object_detection.web.dependencies import camera
from vision_object_detection.web.routes import camera as camera_routes
from vision_object_detection.web.routes import detection, pages, stream


app = FastAPI(title="Vision Object Detection")
app.add_middleware(GZipMiddleware, minimum_size=1000)

BASE_DIR = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
app.include_router(pages.router)
app.include_router(camera_routes.router)
app.include_router(detection.router)
app.include_router(stream.router)


@app.on_event("shutdown")
def shutdown_camera() -> None:
    camera.stop()
