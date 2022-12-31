#!/usr/bin/env python
# coding:utf-8

import datetime
import enum
import locale
import socket
import time

from akari_client import AkariClient
from akari_client.color import Colors
from akari_client.position import Positions


class DisplayMode(int, enum.Enum):
    NONE = 0
    CONNECTION_MODE = 1
    LOGO_MODE = 2
    CLOCK_MODE = 3


duration = 0.01
INPUT_INTERVAL = 1  # ボタン再入力受付時間[s]
akari = AkariClient()
m5 = akari.m5stack
disp_mode = DisplayMode.NONE


def init_connection_disp() -> None:
    connect_interface = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    m5.set_display_color(Colors.WHITE)
    m5.set_display_text(
        text="Console Address",
        pos_y=20,
        size=2,
        text_color=Colors.BLACK,
        back_color=Colors.WHITE,
        refresh=True,
    )
    try:
        connect_interface.connect(("8.8.8.8", 80))
        ip = connect_interface.getsockname()[0]
        address = ip + ":8080"
        m5.set_display_text(
            text=address,
            size=2,
            text_color=Colors.BLACK,
            back_color=Colors.WHITE,
            refresh=False,
        )
    except OSError:
        m5.set_display_text(
            text="Network not found",
            size=2,
            text_color=Colors.RED,
            back_color=Colors.WHITE,
            refresh=False,
        )


def init_clock_disp() -> None:
    m5.set_display_color(Colors.BLACK)
    locale.setlocale(locale.LC_TIME, "ja_JP.UTF-8")
    dt_now = datetime.datetime.now()
    m5.set_display_text(
        text=dt_now.strftime("%Y/%m/%d %a"),
        pos_y=Positions.TOP,
        size=2,
        text_color=Colors.WHITE,
        back_color=Colors.BLACK,
        refresh=True,
    )


def update_clock_disp() -> None:
    dt_now = datetime.datetime.now()
    m5.set_display_text(
        text=dt_now.strftime("%H:%M:%S "),
        size=4,
        text_color=Colors.WHITE,
        back_color=Colors.BLACK,
        refresh=False,
    )


def init_logo_disp() -> None:
    m5.set_display_image("/jpg/logo320.jpg")


def chenge_mode() -> None:
    global disp_mode
    data = m5.get()
    if data["button_a"] and disp_mode != DisplayMode.CONNECTION_MODE:
        init_connection_disp()
        disp_mode = DisplayMode.CONNECTION_MODE
    elif data["button_b"] and disp_mode != DisplayMode.LOGO_MODE:
        init_logo_disp()
        disp_mode = DisplayMode.LOGO_MODE
    elif data["button_c"] and disp_mode != DisplayMode.CLOCK_MODE:
        init_clock_disp()
        disp_mode = DisplayMode.CLOCK_MODE


def display_update() -> None:
    if disp_mode == DisplayMode.CLOCK_MODE:
        update_clock_disp()


def main() -> None:
    while True:
        chenge_mode()
        display_update()
        time.sleep(0.01)


if __name__ == "__main__":
    main()
