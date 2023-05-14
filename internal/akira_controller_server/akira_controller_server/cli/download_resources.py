from akira_controller_server.captures.oakd_face_detection import FaceDetectionCapture
from akira_controller_server.captures.oakd_object_detection import (
    ObjectDetectionCapture,
)


def download_zoo_models() -> None:
    FaceDetectionCapture._get_model_path()
    ObjectDetectionCapture._get_model_path()


if __name__ == "__main__":
    download_zoo_models()
