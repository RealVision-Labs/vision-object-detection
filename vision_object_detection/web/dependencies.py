from vision_object_detection.camera.opencv_camera import OpenCVCamera
from vision_object_detection.detection.factory import create_detector
from vision_object_detection.detection.settings import DetectionSettings


camera = OpenCVCamera()
detector_bundle = create_detector()
detector = detector_bundle.detector
settings = DetectionSettings()
