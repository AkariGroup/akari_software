import asyncio
import contextlib
import enum
import logging
import threading
import time
from typing import AsyncIterator, Optional, Protocol, Tuple

import cv2
import numpy

from .captures.nop import NopCapture
from .captures.oakd_depth import DepthCapture
from .captures.oakd_face_detection import FaceDetectionCapture
from .captures.oakd_object_detection import ObjectDetectionCapture
from .captures.oakd_rgb import RGBCapture

_logger = logging.getLogger(__name__)


def _create_frame(text: str) -> bytes:
    frame = numpy.zeros((480, 640, 3))
    cv2.putText(
        frame,
        text,
        (100, int(frame.shape[0] / 2)),
        cv2.FONT_HERSHEY_SIMPLEX,
        2,
        (255, 255, 255),
        5,
    )
    _, buffer = cv2.imencode(".bmp", frame)
    return buffer.tobytes()


_NOW_LOADING_FRAME = _create_frame("Now Loading...")
_ERROR_FRAME = _create_frame("Error")
_STATIC_FRAME_STAMP = -1


class CaptureProtocol(Protocol):
    def get_frame(self) -> Optional[numpy.ndarray]:
        ...

    def close(self) -> None:
        ...


class CaptureMode(str, enum.Enum):
    NONE = "None"
    RGB = "RGB"
    DEPTH = "Depth"
    FACE_DETECTION = "FaceDetection"
    OBJECT_DETECTION = "ObjectDetection"


def capture_factory(mode: CaptureMode) -> CaptureProtocol:
    if mode is CaptureMode.NONE:
        return NopCapture()
    elif mode is CaptureMode.RGB:
        return RGBCapture()
    elif mode is CaptureMode.DEPTH:
        return DepthCapture()
    elif mode is CaptureMode.FACE_DETECTION:
        return FaceDetectionCapture()
    elif mode is CaptureMode.OBJECT_DETECTION:
        return ObjectDetectionCapture()


class SubscriptionCounter:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._num_subscribers = 0

    def notify_subscribe(self) -> None:
        with self._lock:
            self._num_subscribers += 1

    def notify_unsubscribe(self) -> None:
        with self._lock:
            self._num_subscribers -= 1

    def is_subscribed(self) -> bool:
        return self._num_subscribers > 0

    def wait_for_subscription(self) -> None:
        while not self.is_subscribed():
            time.sleep(0.01)


class MediaController:
    def __init__(self) -> None:
        self._mode = CaptureMode.NONE
        self._subscriptions = SubscriptionCounter()
        self._producer_frequency = 10

        self._latest_frame = b""
        self._latest_frame_stamp = 0.0

        self._lock = threading.Lock()
        self._closed = False
        self._thread = threading.Thread(target=self._produce)
        self._thread.start()

    def close(self) -> None:
        self._closed = True
        self._thread.join()

    @property
    def mode(self) -> CaptureMode:
        return self._mode

    def switch_mode(self, mode: CaptureMode) -> None:
        self._mode = mode

    def _update_frame(self, frame: bytes, stamp: float) -> None:
        with self._lock:
            self._latest_frame = frame
            self._latest_frame_stamp = stamp

    def _produce_core(self, capture: CaptureProtocol, mode: CaptureMode) -> None:
        interval = 1.0 / self._producer_frequency
        while (
            not self._closed
            and mode == self._mode
            and self._subscriptions.is_subscribed()
        ):
            next_interval = time.time() + interval

            frame = capture.get_frame()
            if frame is not None:
                _, buffer = cv2.imencode(".bmp", frame)
                frame_data = buffer.tobytes()

                self._update_frame(frame_data, time.time())

            sleep_sec = next_interval - time.time()
            if sleep_sec > 0:
                time.sleep(sleep_sec)

    def _produce(self) -> None:
        while not self._closed:
            self._update_frame(_NOW_LOADING_FRAME, _STATIC_FRAME_STAMP)
            self._subscriptions.wait_for_subscription()
            with contextlib.ExitStack() as stack:
                mode = self._mode
                _logger.info(f"producer started: {mode}")
                try:
                    capture = capture_factory(mode)
                    stack.enter_context(contextlib.closing(capture))
                    self._produce_core(capture, mode)
                    self._update_frame(_NOW_LOADING_FRAME, _STATIC_FRAME_STAMP)
                except Exception:
                    _logger.exception("unhandled exception")
                    self._update_frame(_ERROR_FRAME, _STATIC_FRAME_STAMP)
                    # NOTE: sleep 0.5 seconds for the next trial
                    time.sleep(0.5)

                _logger.info("producer paused")

    async def _get_latest_frame(self, previous_stamp: float) -> Tuple[bytes, float]:
        frame: bytes
        stamp: float

        while not self._closed:
            with self._lock:
                # NOTE: No producer exists when time_stamp is a negative value.
                # Some browsers don't update the content if the API returns a single frame.
                # Thus, we return the same frame multiple times in this case.
                if (
                    self._latest_frame_stamp != previous_stamp
                    or self._latest_frame_stamp < 0
                ):
                    frame = self._latest_frame
                    stamp = self._latest_frame_stamp
                    break

            await asyncio.sleep(0.01)

        # NOTE: Suppress frequent update request
        if stamp < 0:
            await asyncio.sleep(0.1)

        return frame, stamp

    async def consumer(self) -> AsyncIterator[bytes]:
        self._subscriptions.notify_subscribe()
        try:
            handled_stamp = 0.0
            while True:
                frame, handled_stamp = await self._get_latest_frame(handled_stamp)
                yield (b"--frame\r\nContent-Type: image/bmp\r\n\r\n" + frame + b"\r\n")
        finally:
            self._subscriptions.notify_unsubscribe()
