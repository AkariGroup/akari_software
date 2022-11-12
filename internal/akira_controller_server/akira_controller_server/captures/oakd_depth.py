import contextlib
from typing import Optional

import cv2
import depthai as dai
import numpy

MAX_DEPTH = 1500.0  # unit: [mm]


def _get_colored_depth(depth: numpy.ndarray) -> numpy.ndarray:
    depth[numpy.where(depth > MAX_DEPTH)] = 0
    norm_depth = (depth * (255 / MAX_DEPTH)).astype(numpy.uint8)
    colored_depth: numpy.ndarray = cv2.applyColorMap(norm_depth, cv2.COLORMAP_JET)
    return colored_depth


class DepthCapture:
    @staticmethod
    def _create_pipeline() -> dai.Pipeline:
        pipeline = dai.Pipeline()

        # camera setting
        camera_left = pipeline.create(dai.node.MonoCamera)
        camera_left.setResolution(dai.MonoCameraProperties.SensorResolution.THE_480_P)
        camera_right = pipeline.create(dai.node.MonoCamera)
        camera_right.setResolution(dai.MonoCameraProperties.SensorResolution.THE_480_P)

        stereo_camera = pipeline.create(dai.node.StereoDepth)
        camera_left.out.link(stereo_camera.left)
        camera_right.out.link(stereo_camera.right)

        # video setting
        video = pipeline.create(dai.node.XLinkOut)
        video.setStreamName("video")
        stereo_camera.depth.link(video.input)

        return pipeline

    def __init__(self) -> None:
        self._stack = contextlib.ExitStack()
        self._pipeline = DepthCapture._create_pipeline()
        self._device = self._stack.enter_context(
            dai.Device(self._pipeline, usb2Mode=True)
        )
        self._video: Optional[dai.DataOutputQueue] = self._device.getOutputQueue(  # type: ignore
            name="video",
            maxSize=4,
            blocking=False,
        )

    def get_frame(self) -> Optional[numpy.ndarray]:
        video = self._video
        if video is None:
            return None
        frame: Optional[numpy.ndarray] = video.get().getCvFrame()  # type: ignore
        if frame is None:
            return None
        return _get_colored_depth(frame)

    def close(self) -> None:
        self._stack.close()
        self._video = None
