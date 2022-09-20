from __future__ import annotations

import enum


class Positions(int, enum.Enum):
    CENTER = -999
    LEFT = 0
    TOP = 0
    RIGHT = 999
    BOTTOM = 999