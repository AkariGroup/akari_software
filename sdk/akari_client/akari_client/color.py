from __future__ import annotations

import dataclasses
import enum


@dataclasses.dataclass(frozen=True)
class Color:
    """M5のディスプレイの表示色を指定するクラス。

    :param red: RGBのR要素。0~255で指定。
    :param green: RGBのG要素。0~255で指定。
    :param blue: RGBのB要素。0~255で指定。

    """

    red: int
    green: int
    blue: int

    def __post_init__(self) -> None:
        assert 0 <= self.red <= 0xFF
        assert 0 <= self.green <= 0xFF
        assert 0 <= self.blue <= 0xFF

    @staticmethod
    def from_rgb565(value: int) -> Color:
        # NOTE: Colors in RGB565 are represented as follows
        # value = (r7 r6 r5 r4 r3 g7 g6 g5 g4 g3 g2 b7 b6 b5 b4 b3)
        assert 0 <= value <= 0xFFFF
        blue = (value & 0x1F) << 3
        # lshift 5 bits and rshift 2 bits
        green = (value & 0x7E0) >> 3
        # lshift 11 bits and rshift 3 bits
        red = (value & 0xF800) >> 8

        return Color(red, green, blue)

    def as_rgb565(self) -> int:
        return ((self.red >> 3) << 11) | ((self.green >> 2) << 5) | (self.blue >> 3)


class Colors(Color, enum.Enum):
    """
    | M5のディスプレイの表示色のenum。
    | 下記の色を指定可能。
    | BLACK
    | NAVY
    | DARKGREEN
    | DARKCYAN
    | MAROON
    | PURPLE
    | OLIVE
    | LIGHTGREY
    | DARKGREY
    | BLUE
    | GREEN
    | CYAN
    | RED
    | MAGENTA
    | YELLOW
    | WHITE
    | ORANGE
    | GREENYELLOW
    | PINK

    """

    BLACK = (0, 0, 0)
    NAVY = (0, 0, 127)
    DARKGREEN = (0, 127, 0)
    DARKCYAN = (0, 127, 127)
    MAROON = (127, 0, 0)
    PURPLE = (127, 0, 127)
    OLIVE = (127, 127, 0)
    LIGHTGREY = (192, 192, 192)
    DARKGREY = (127, 127, 127)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    CYAN = (0, 255, 0)
    RED = (255, 0, 0)
    MAGENTA = (255, 0, 255)
    YELLOW = (255, 255, 0)
    WHITE = (255, 255, 255)
    ORANGE = (255, 165, 0)
    GREENYELLOW = (173, 255, 47)
    PINK = (255, 0, 255)
