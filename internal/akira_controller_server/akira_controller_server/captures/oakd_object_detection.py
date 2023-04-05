import contextlib
import pathlib
from typing import Any, Optional, Tuple

import cv2
import depthai as dai
import numpy

PACKAGE_DIR = pathlib.Path(__file__).resolve().parents[2]
WEIGHT_PATH = (
    PACKAGE_DIR / "data/object_detection/mobilenet-ssd_openvino_2021.4_6shave.blob"
)

WIDTH = 300
HEIGHT = 300
CONFIDENCE_THRESHOLD = 0.5
LABEL_MAP = [
    "background",
    "aeroplane",
    "bicycle",
    "bird",
    "boat",
    "bottle",
    "bus",
    "car",
    "cat",
    "chair",
    "cow",
    "diningtable",
    "dog",
    "horse",
    "motorbike",
    "person",
    "pottedplant",
    "sheep",
    "sofa",
    "train",
    "tvmonitor",
]
numpy.random.seed(7)
COLOR_MAP = numpy.random.randint(0, 255, (len(LABEL_MAP), 3))


def _get_norm_bbox(
    bbox: Tuple[float, float, float, float]
) -> Tuple[int, int, int, int]:
    norm_box: Tuple[int, int, int, int] = (
        numpy.clip(numpy.array(bbox), 0, 1)
        * numpy.array([WIDTH, HEIGHT, WIDTH, HEIGHT])
    ).astype(int)
    return norm_box


def _render_frame(name: str, frame: numpy.ndarray, detections: Any) -> numpy.ndarray:
    for detection in detections:
        bbox = _get_norm_bbox(
            (detection.xmin, detection.ymin, detection.xmax, detection.ymax)
        )
        detection_label = detection.label
        color = COLOR_MAP[detection_label].tolist()
        cv2.putText(
            frame,
            LABEL_MAP[detection_label],
            (bbox[0] + 10, bbox[1] + 20),
            cv2.FONT_HERSHEY_TRIPLEX,
            0.5,
            color,
        )
        cv2.putText(
            frame,
            f"{int(detection.confidence * 100)}%",
            (bbox[0] + 10, bbox[1] + 40),
            cv2.FONT_HERSHEY_TRIPLEX,
            0.5,
            color,
        )
        cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), color, 2)
    resized_frame: numpy.ndarray = cv2.resize(frame, (640, 480))
    return resized_frame


class ObjectDetectionCapture:
    @staticmethod
    def _create_pipeline() -> dai.Pipeline:
        pipeline = dai.Pipeline()

        # Define sources and outputs
        camera_rgb = pipeline.create(dai.node.ColorCamera)
        nn = pipeline.create(dai.node.MobileNetDetectionNetwork)

        rgb_out = pipeline.create(dai.node.XLinkOut)
        nn_out = pipeline.create(dai.node.XLinkOut)
        rgb_out.setStreamName("rgb")
        nn_out.setStreamName("nn")

        # Properties
        camera_rgb.setPreviewSize(WIDTH, HEIGHT)
        camera_rgb.setInterleaved(False)
        camera_rgb.setFps(30)

        nn.setConfidenceThreshold(CONFIDENCE_THRESHOLD)
        nn.setBlobPath(WEIGHT_PATH)
        nn.setNumInferenceThreads(2)
        nn.input.setBlocking(False)

        camera_rgb.preview.link(rgb_out.input)
        camera_rgb.preview.link(nn.input)
        nn.out.link(nn_out.input)

        return pipeline

    def __init__(self) -> None:
        self._stack = contextlib.ExitStack()
        self._pipeline = ObjectDetectionCapture._create_pipeline()
        self._device = self._stack.enter_context(
            dai.Device(self._pipeline, usb2Mode=True)
        )
        self._rgb_queue = self._device.getOutputQueue(  # type: ignore
            name="rgb", maxSize=4, blocking=False
        )
        self._detection_queue = self._device.getOutputQueue(  # type: ignore
            name="nn", maxSize=4, blocking=False
        )

    def get_frame(self) -> Optional[numpy.ndarray]:
        rgb_queue = self._rgb_queue
        detection_queue = self._detection_queue

        if rgb_queue is None or detection_queue is None:
            return None

        frame: Optional[numpy.ndarray] = rgb_queue.get().getCvFrame()  # type: ignore
        detection: Optional[Any] = detection_queue.get().detections
        if frame is None or detection is None:
            return None
        return _render_frame("rgb", frame, detection)

    def close(self) -> None:
        self._stack.close()
        self._rgb_queue = None
        self._detection_queue = None
