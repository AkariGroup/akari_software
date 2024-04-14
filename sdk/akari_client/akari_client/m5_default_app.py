#!/usr/bin/env python
# coding:utf-8

import datetime
import enum
import locale
import socket
import time

from serial.m5stack import M5StackSerialClient
from akari_client.color import Colors
from akari_client.position import Positions


class DisplayMode(int, enum.Enum):
    NONE = 0
    CONNECTION_MODE = 1
    LOGO_MODE = 2
    CLOCK_MODE = 3


class DefaultApp(object):
    def __init__(self, client: M5StackSerialClient):
        self.client = client
        self.disp_mode = DisplayMode.NONE
        self.is_running = True
        self.run()

    def init_connection_disp(self) -> None:
        connect_interface = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client.set_display_color(Colors.WHITE)
        self.client.set_display_text(
            text="Console Address",
            pos_y=20,
            size=3,
            text_color=Colors.BLACK,
            back_color=Colors.WHITE,
            refresh=True,
        )
        try:
            connect_interface.connect(("8.8.8.8", 80))
            ip = connect_interface.getsockname()[0]
            address = ip + ":8080"
            self.client.set_display_text(
                text=address,
                size=2,
                text_color=Colors.BLACK,
                back_color=Colors.WHITE,
                refresh=False,
            )
        except OSError:
            self.client.set_display_text(
                text="Network not found",
                size=2,
                text_color=Colors.RED,
                back_color=Colors.WHITE,
                refresh=False,
            )

    def init_clock_disp(self) -> None:
        self.client.set_display_color(Colors.BLACK)
        locale.setlocale(locale.LC_TIME, "ja_JP.UTF-8")
        dt_now = datetime.datetime.now()
        self.client.set_display_text(
            text=dt_now.strftime("%Y/%m/%d %a"),
            pos_y=Positions.TOP,
            size=3,
            text_color=Colors.WHITE,
            back_color=Colors.BLACK,
            refresh=True,
        )

    def update_clock_disp(self) -> None:
        dt_now = datetime.datetime.now()
        self.client.set_display_text(
            text=dt_now.strftime("%H:%M:%S "),
            size=7,
            text_color=Colors.WHITE,
            back_color=Colors.BLACK,
            refresh=False,
        )

    def init_logo_disp(self) -> None:
        self.client.set_display_image("/jpg/logo320.jpg")

    def chenge_mode(self) -> None:
        data = self.client.get()
        if data["button_a"] and self.disp_mode != DisplayMode.CONNECTION_MODE:
            self.init_connection_disp()
            self.disp_mode = DisplayMode.CONNECTION_MODE
        elif data["button_b"] and self.disp_mode != DisplayMode.LOGO_MODE:
            self.init_logo_disp()
            self.disp_mode = DisplayMode.LOGO_MODE
        elif data["button_c"] and self.disp_mode != DisplayMode.CLOCK_MODE:
            self.init_clock_disp()
            self.disp_mode = DisplayMode.CLOCK_MODE

    def display_update(self) -> None:
        if self.disp_mode == DisplayMode.CLOCK_MODE:
            self.update_clock_disp()

    def run(self) -> None:
        while self.is_running:
            self.chenge_mode()
            self.display_update()
            time.sleep(0.01)
        self.client.set_display_image("/jpg/logo320.jpg")

    def stop(self) -> None:
        self.is_running = False
