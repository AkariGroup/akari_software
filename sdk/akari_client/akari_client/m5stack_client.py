from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional, TypedDict

from .color import Color


class M5ComDict(TypedDict):
    din0: bool
    din1: bool
    ain0: int
    dout0: bool
    dout1: bool
    pwmout0: int
    general0: float
    general1: float
    button_a: bool
    button_b: bool
    button_c: bool
    temperature: float
    pressure: float
    brightness: int
    time: float
    is_response: bool


class M5StackClient(ABC):
    @abstractmethod
    def set_dout(self, pin_id: int, value: bool, sync: bool = True) -> None:
        ...

    @abstractmethod
    def set_pwmout(self, pin_id: int, value: int, sync: bool = True) -> None:
        ...

    @abstractmethod
    def set_allout(
        self,
        *,
        dout0: bool,
        dout1: bool,
        pwmout0: int,
        sync: bool = True,
    ) -> None:
        ...

    @abstractmethod
    def reset_allout(self, sync: bool = True) -> None:
        ...

    @abstractmethod
    def set_display_color(
        self,
        color: Color,
        sync: bool = True,
    ) -> None:
        ...

    @abstractmethod
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
        ...

    @abstractmethod
    def set_display_image(
        self,
        filepath: str,
        pos_x: int,
        pos_y: int,
        scale: float,
        sync: bool = True,
    ) -> None:
        ...

    @abstractmethod
    def use_japanese_font(
        self,
        enabled: bool,
        sync: bool = True,
    ) -> None:
        ...

    @abstractmethod
    def reset_m5(self) -> None:
        ...

    @abstractmethod
    def get(self) -> M5ComDict:
        ...
