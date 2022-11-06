from typing import Optional

import numpy


class NopCapture:
    FRAME = numpy.zeros((480, 640, 3), dtype=numpy.uint8)

    def get_frame(self) -> Optional[numpy.ndarray]:
        return NopCapture.FRAME

    def close(self) -> None:
        pass
