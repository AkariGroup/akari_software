from __future__ import annotations

import contextlib
import time
from typing import Any, List, Optional, Tuple

from .m5serial_communicator import M5ComDict, M5SerialCommunicator

"""
m5serial_server_py
Created on 2020/05/08
@author: Kazuya Yamamoto
"""

RESETALLOUT = 0
WRITEPINVAL = 1
SETDISPLAYCOLOR = 10
SETDISPLAYTEXT = 11
SETDISPLAYIMG = 12
USEJAPANESEFONT = 13
RESETM5 = 99
STARTM5 = 98
color_pair: List[Tuple[str, int]] = [
    ("black", 0x0000),
    ("navy", 0x000F),
    ("darkgreen", 0x03E0),
    ("darkcyan", 0x03EF),
    ("maroon", 0x7800),
    ("purple", 0x780F),
    ("olive", 0x7BE0),
    ("lightgrey", 0xC618),
    ("darkgrey", 0x7BEF),
    ("blue", 0x001F),
    ("green", 0x07E0),
    ("cyan", 0x07E0),
    ("red", 0xF800),
    ("magenta", 0xF81F),
    ("yellow", 0xFFE0),
    ("white", 0xFFFF),
    ("orange", 0xFD20),
    ("greenyellow", 0xAFE5),
    ("pink", 0xF81F),
]


class M5SerialServer:
    def __init__(self, communicator: Optional[M5SerialCommunicator] = None) -> None:
        self._stack = contextlib.ExitStack()
        if communicator is None:
            self._communicator = self._stack.enter_context(M5SerialCommunicator())
        else:
            self._communicator = communicator

        self.__dout0_val = 0
        self.__dout1_val = 0
        self.__pwmout0_val = 0
        self.__data_str: str = ""
        self.reset_m5()
        self._communicator.start()
        time.sleep(0.1)

    def __enter__(self) -> M5SerialServer:
        return self

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        self.close()

    def close(self) -> None:
        self._stack.close()

    def __color_to_m5code(self, color_str: str) -> int:
        color_int = -1
        for i in range(0, len(color_pair)):
            if color_str == color_pair[i][0]:
                color_int = color_pair[i][1]
                break
        return color_int

    def __write_pinval_command(self, dout0: int, dout1: int, pwmout0: int) -> bool:
        data = {
            "com": WRITEPINVAL,
            "pin": {"do0": dout0, "do1": dout1, "po0": pwmout0},
        }
        result = self._communicator.send_data(data)
        return result

    def __start_m5(self) -> None:
        self.__dout0_val = 0
        self.__dout1_val = 0
        self.__pwmout0_val = 0
        data = {"com": 98}
        assert self._communicator.send_data(data)
        time.sleep(0.1)

    def set_dout(self, pin_id: int, val: bool, sync_flg: bool = True) -> int:
        if pin_id == 0:
            self.__dout0_val = int(val)
        elif pin_id == 1:
            self.__dout1_val = int(val)
        else:
            return 0
        result = self.__write_pinval_command(
            self.__dout0_val, self.__dout1_val, self.__pwmout0_val
        )
        self._communicator.wait_sync(sync_flg)
        return result

    def set_pwmout(self, pin_id: int, val: int, sync_flg: bool = True) -> int:
        if pin_id == 0:
            self.__pwmout0_val = int(val)
        else:
            return 0
        result = self.__write_pinval_command(
            self.__dout0_val, self.__dout1_val, self.__pwmout0_val
        )
        self._communicator.wait_sync(sync_flg)
        return result

    def set_allout(
        self, dout0_val: bool, dout1_val: bool, pwmout0_val: int, sync_flg: bool = True
    ) -> bool:
        self.__dout0_val = int(dout0_val)
        self.__dout1_val = int(dout1_val)
        self.__pwmout0_val = int(pwmout0_val)
        result = self.__write_pinval_command(
            self.__dout0_val, self.__dout1_val, self.__pwmout0_val
        )
        self._communicator.wait_sync(sync_flg)
        return result

    def reset_allout(self, sync_flg: bool = True) -> bool:
        self.__dout0_val = 0
        self.__dout1_val = 0
        self.__pwmout0_val = 0
        data = {"com": RESETALLOUT}
        result = self._communicator.send_data(data)
        self._communicator.wait_sync(sync_flg)
        return result

    def set_display_color(self, color: str, sync_flg: bool = True) -> bool:
        data = {
            "com": SETDISPLAYCOLOR,
            "lcd": {"cl": self.__color_to_m5code(color)},
        }
        result = self._communicator.send_data(data)
        self._communicator.wait_sync(sync_flg)
        return result

    def set_display_text(
        self,
        text: str,
        pos_x: int,
        pos_y: int,
        size: int,
        text_color: str,
        back_color: str,
        refresh: bool,
        sync_flg: bool = True,
    ) -> bool:
        data = {
            "com": SETDISPLAYTEXT,
            "lcd": {
                "m": text,
                "x": pos_x,
                "y": pos_y,
                "sz": size,
                "cl": self.__color_to_m5code(text_color),
                "bk": self.__color_to_m5code(back_color),
                "rf": int(refresh),
            },
        }
        result = self._communicator.send_data(data)
        self._communicator.wait_sync(sync_flg)
        return result

    def set_display_image(
        self, filepath: str, pos_x: int, pos_y: int, scale: float, sync_flg: bool = True
    ) -> bool:
        data = {
            "com": SETDISPLAYIMG,
            "lcd": {"pth": filepath, "x": pos_x, "y": pos_y, "scl": round(scale, 2)},
        }
        result = self._communicator.send_data(data)
        self._communicator.wait_sync(sync_flg)
        return result

    def use_japanese_font(self, enabled: bool, sync_flg: bool = True) -> bool:
        data = {"com": USEJAPANESEFONT, "lcd": {"jp": enabled}}
        result = self._communicator.send_data(data)
        self._communicator.wait_sync(sync_flg)
        return result

    def reset_m5(self) -> bool:
        self.__dout0_val = 0
        self.__dout1_val = 0
        self.__pwmout0_val = 0
        data = {"com": 99}
        result = self._communicator.send_data(data)
        time.sleep(2)
        self.__start_m5()
        return result

    def get(self) -> M5ComDict:
        return self._communicator.get()
