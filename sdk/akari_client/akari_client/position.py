from __future__ import annotations

import enum


class Positions(int, enum.Enum):
    """
    | M5のディスプレイの表示位置のenum。
    | 下記が利用可能。
    | CENTER: 中央
    | LEFT: 左揃え
    | TOP: 上揃え
    | RIGHT: 右揃え
    | BOTTOM: 下揃え

    """

    CENTER = -999
    LEFT = 0
    TOP = 0
    RIGHT = 999
    BOTTOM = 999
