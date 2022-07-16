from __future__ import annotations

import contextlib
import dataclasses
import enum
import time
from typing import Any, Dict, Optional

from .color import Color
from .m5serial_communicator import M5ComDict, M5SerialCommunicator

"""
m5serial_server_py
Created on 2020/05/08
@author: Kazuya Yamamoto
"""


class CommandId(enum.IntEnum):
    RESETALLOUT = 0
    WRITEPINVAL = 1
    SETDISPLAYCOLOR = 10
    SETDISPLAYTEXT = 11
    SETDISPLAYIMG = 12
    USEJAPANESEFONT = 13
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


class M5SerialServer:
    def __init__(self, communicator: Optional[M5SerialCommunicator] = None) -> None:
        self._stack = contextlib.ExitStack()
        if communicator is None:
            self._communicator = self._stack.enter_context(M5SerialCommunicator())
        else:
            self._communicator = communicator

        self._pin_out = _PinOut()

        self.reset_m5()
        self._communicator.start()
        time.sleep(0.1)

    def __enter__(self) -> M5SerialServer:
        return self

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        self.close()

    def close(self) -> None:
        self._stack.close()

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
        dout0: bool,
        dout1: bool,
        pwmout0: int,
        sync: bool = True,
    ) -> None:
        self._pin_out.dout0 = dout0
        self._pin_out.dout1 = dout1
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
        pos_x: int,
        pos_y: int,
        size: int,
        text_color: Optional[Color] = None,
        back_color: Optional[Color] = None,
        refresh: bool = False,
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
        self, filepath: str, pos_x: int, pos_y: int, scale: float, sync: bool = True
    ) -> None:
        data = {
            "com": CommandId.SETDISPLAYIMG,
            "lcd": {"pth": filepath, "x": pos_x, "y": pos_y, "scl": round(scale, 2)},
        }
        self._communicator.send_data(data, sync)

    def use_japanese_font(self, enabled: bool, sync: bool = True) -> None:
        data = {"com": CommandId.USEJAPANESEFONT, "lcd": {"jp": enabled}}
        self._communicator.send_data(data, sync)

    def reset_m5(self) -> None:
        data = {"com": CommandId.RESETM5}
        self._communicator.send_data(data, sync=False)
        self._pin_out.reset()
        time.sleep(2)
        self._start_m5()

    def get(self) -> M5ComDict:
        return self._communicator.get()
