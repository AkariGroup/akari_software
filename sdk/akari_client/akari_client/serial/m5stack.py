from __future__ import annotations

import dataclasses
import enum
import time
from typing import Any, Dict, Optional

from ..color import Color
from ..m5stack_client import M5ComDict, M5StackClient
from ..position import Positions
from .m5stack_communicator import M5SerialCommunicator


class CommandId(enum.IntEnum):
    RESETALLOUT = 0
    WRITEPINVAL = 1
    SETDISPLAYCOLOR = 10
    SETDISPLAYTEXT = 11
    SETDISPLAYIMG = 12
    STARTM5 = 98
    RESETM5 = 99


@dataclasses.dataclass
class _PinOut:
    dout0: bool = False
    dout1: bool = False
    pwmout0: int = 0

    def reset(self) -> None:
        self.dout0 = False
        self.dout1 = False
        self.pwmout0 = 0

    def serialize(self) -> Dict[str, Any]:
        return {"do0": int(self.dout0), "do1": int(self.dout1), "po0": self.pwmout0}


class M5StackSerialClient(M5StackClient):
    def __init__(self, communicator: M5SerialCommunicator) -> None:
        self._communicator = communicator

        self._pin_out = _PinOut()
        self.reset_m5()
        self._communicator.start()
        time.sleep(0.1)

    def _write_pin_out(self, sync: bool) -> None:
        data = {
            "com": CommandId.WRITEPINVAL,
            "pin": self._pin_out.serialize(),
        }
        self._communicator.send_data(data, sync=sync)

    def _start_m5(self) -> None:
        data = {"com": CommandId.STARTM5}
        self._communicator.send_data(data, sync=False)
        self._pin_out.reset()
        time.sleep(0.1)

    def set_dout(self, pin_id: int, value: bool, sync: bool = True) -> None:
        if pin_id == 0:
            self._pin_out.dout0 = value
        elif pin_id == 1:
            self._pin_out.dout1 = value
        else:
            raise ValueError(f"Out of range pin_id: {pin_id}")

        self._write_pin_out(sync=sync)

    def set_pwmout(self, pin_id: int, value: int, sync: bool = True) -> None:
        if pin_id == 0:
            self._pin_out.pwmout0 = value
        else:
            raise ValueError(f"Out of range pin_id: {pin_id}")

        self._write_pin_out(sync=sync)

    def set_allout(
        self,
        *,
        dout0: Optional[bool] = None,
        dout1: Optional[bool] = None,
        pwmout0: Optional[int] = None,
        sync: bool = True,
    ) -> None:
        if dout0 is not None:
            self._pin_out.dout0 = dout0
        if dout1 is not None:
            self._pin_out.dout1 = dout1
        if pwmout0 is not None:
            self._pin_out.pwmout0 = pwmout0

        self._write_pin_out(sync=sync)

    def reset_allout(self, sync: bool = True) -> None:
        self._pin_out.reset()
        data = {"com": CommandId.RESETALLOUT}
        self._communicator.send_data(data, sync)

    def set_display_color(self, color: Color, sync: bool = True) -> None:
        data = {
            "com": CommandId.SETDISPLAYCOLOR,
            "lcd": {"cl": color.as_rgb565()},
        }
        self._communicator.send_data(data, sync)

    def set_display_text(
        self,
        text: str,
        pos_x: int = Positions.CENTER,
        pos_y: int = Positions.CENTER,
        size: int = 5,
        text_color: Optional[Color] = None,
        back_color: Optional[Color] = None,
        refresh: bool = True,
        sync: bool = True,
    ) -> None:
        text_color_value = -1
        bg_color_value = -1

        if text_color is not None:
            text_color_value = text_color.as_rgb565()
        if back_color is not None:
            bg_color_value = back_color.as_rgb565()

        data = {
            "com": CommandId.SETDISPLAYTEXT,
            "lcd": {
                "m": text,
                "x": pos_x,
                "y": pos_y,
                "sz": size,
                "cl": text_color_value,
                "bk": bg_color_value,
                "rf": int(refresh),
            },
        }
        self._communicator.send_data(data, sync)

    def set_display_image(
        self,
        filepath: str,
        pos_x: int = Positions.CENTER,
        pos_y: int = Positions.CENTER,
        scale: float = -1.0,
        sync: bool = True,
    ) -> None:
        data = {
            "com": CommandId.SETDISPLAYIMG,
            "lcd": {"pth": filepath, "x": pos_x, "y": pos_y, "scl": round(scale, 2)},
        }
        self._communicator.send_data(data, sync)

    def reset_m5(self) -> None:
        data = {"com": CommandId.RESETM5}
        self._communicator.send_data(data, sync=False)
        self._pin_out.reset()
        time.sleep(4)
        self._start_m5()

    def get(self) -> M5ComDict:
        return self._communicator.get()
