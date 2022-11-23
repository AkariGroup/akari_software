from __future__ import annotations

import enum


class Positions(int, enum.Enum):
    """M5のディスプレイの表示位置のenum。"""

    CENTER = -999
    LEFT = 0
    TOP = 0
    RIGHT = 999
    BOTTOM = 999
