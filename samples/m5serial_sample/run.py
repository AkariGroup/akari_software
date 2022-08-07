#!/usr/bin/env python
# coding:utf-8

"""
m5serial_sample_py
Created on 2020/05/15
@author: Kazuya Yamamoto
"""

import datetime
import locale
import time

from akari_client import AkariClient
from akari_client.m5stack_client import M5StackClient
from akari_client.color import Colors

CLOCK_MODE = 1
SENSOR_MODE = 2
IO_MODE = 3
duration = 0.01
INPUT_INTERVAL = 1  # ボタン再入力受付時間[s]


class M5serialSample(object):
    def __init__(self, m5: M5StackClient) -> None:
        self.m5 = m5

        self.is_initializing = False
        self.button_a_input_time = datetime.datetime.now()
        self.button_b_input_time = datetime.datetime.now()
        self.button_c_input_time = datetime.datetime.now()
        self.disp_mode = 0
        # m5.reset_m5()

    def init_clock_disp(self) -> None:
        global duration
        duration = 0.5
        self.m5.set_display_color(Colors.BLACK)
        locale.setlocale(locale.LC_TIME, "ja_JP.UTF-8")
        dt_now = datetime.datetime.now()
        self.m5.set_display_text(
            dt_now.strftime("%Y/%m/%d %a"),
            -999,
            0,
            2,
            text_color=Colors.WHITE,
            back_color=Colors.BLACK,
            refresh=True,
        )
        self.is_initializing = False

    def update_clock_disp(self) -> None:
        if self.disp_mode == CLOCK_MODE:
            dt_now = datetime.datetime.now()
            self.m5.set_display_text(
                dt_now.strftime("%H:%M:%S "),
                -999,
                -999,
                4,
                text_color=Colors.WHITE,
                back_color=Colors.BLACK,
            )

    def init_sensor_disp(self) -> None:
        self.m5.set_display_color(Colors.LIGHTGREY)
        self.is_initializing = False

    def update_sensor_disp(self) -> None:
        if self.disp_mode == SENSOR_MODE:
            self.m5.set_display_text(
                "明るさ: " + str(self.brightness).rjust(4, " ") + " \n",
                0,
                20,
                2,
                text_color=Colors.ORANGE,
            )
        if self.disp_mode == SENSOR_MODE:
            self.m5.set_display_text(
                "気圧: " + str(round(self.pressure / 100, 2)).rjust(7, " ") + " hPa  \n",
                0,
                100,
                2,
                text_color=Colors.PINK,
            )
        if self.disp_mode == SENSOR_MODE:
            self.m5.set_display_text(
                "気温: " + str(round(self.temperature, 2)).rjust(7, " ") + " C \n",
                0,
                180,
                2,
                text_color=Colors.PURPLE,
            )

    def init_io_disp(self) -> None:
        self.m5.set_display_color(Colors.WHITE)
        self.is_initializing = False

    def update_io_disp(self) -> None:
        if self.disp_mode == IO_MODE:
            if self.din0:
                self.m5.set_display_text(
                    "din0: " + str(int(self.din0)) + " \n",
                    0,
                    0,
                    2,
                    text_color=Colors.WHITE,
                    back_color=Colors.RED,
                )
            else:
                self.m5.set_display_text(
                    "din0: " + str(int(self.din0)) + "    \n",
                    0,
                    0,
                    2,
                    text_color=Colors.BLACK,
                )
        if self.disp_mode == IO_MODE:
            if self.din1:
                self.m5.set_display_text(
                    "din1: " + str(int(self.din1)) + " \n",
                    0,
                    40,
                    2,
                    text_color=Colors.WHITE,
                    back_color=Colors.RED,
                )
            else:
                self.m5.set_display_text(
                    "din1: " + str(int(self.din1)) + "    \n",
                    0,
                    40,
                    2,
                    text_color=Colors.BLACK,
                )
        if self.disp_mode == IO_MODE:
            if self.ain0 > 0:
                self.m5.set_display_text(
                    "ain0: " + str(int(self.ain0)).rjust(3, " ") + " \n",
                    0,
                    80,
                    2,
                    text_color=Colors.WHITE,
                    back_color=Colors.GREEN,
                )
            else:
                self.m5.set_display_text(
                    "ain0: " + str(int(self.ain0)).rjust(3, " ") + "    \n",
                    0,
                    80,
                    2,
                    text_color=Colors.GREEN,
                )
        if self.disp_mode == IO_MODE:
            if self.dout0:
                self.m5.set_display_text(
                    "dout0: " + str(int(self.dout0)) + " \n",
                    0,
                    120,
                    2,
                    text_color=Colors.WHITE,
                    back_color=Colors.RED,
                )
            else:
                self.m5.set_display_text(
                    "dout0: " + str(int(self.dout0)) + "    \n",
                    0,
                    120,
                    2,
                    text_color=Colors.BLACK,
                )
        if self.disp_mode == IO_MODE:
            if self.dout1:
                self.m5.set_display_text(
                    "dout1: " + str(int(self.dout1)) + " \n",
                    0,
                    160,
                    2,
                    text_color=Colors.WHITE,
                    back_color=Colors.RED,
                )
            else:
                self.m5.set_display_text(
                    "dout1: " + str(int(self.dout1)) + "    \n",
                    0,
                    160,
                    2,
                    text_color=Colors.BLACK,
                )
        if self.disp_mode == IO_MODE:
            if self.pwmout0 > 0:
                self.m5.set_display_text(
                    "pwmout0: " + str(int(self.pwmout0)).rjust(3, " ") + " \n",
                    0,
                    200,
                    2,
                    text_color=Colors.WHITE,
                    back_color=Colors.BLUE,
                )
            else:
                self.m5.set_display_text(
                    "pwmout0: " + str(int(self.pwmout0)).rjust(3, " ") + "    \n",
                    0,
                    200,
                    2,
                    text_color=Colors.BLUE,
                )

    def display_update(self) -> None:
        data = self.m5.get()
        self.din0 = data["din0"]
        self.din1 = data["din1"]
        self.ain0 = data["ain0"]
        self.dout0 = data["dout0"]
        self.dout1 = data["dout1"]
        self.pwmout0 = data["pwmout0"]
        self.pressure = data["pressure"]
        self.temperature = data["temperature"]
        self.brightness = data["brightness"]
        self.time = data["time"]
        if (
            data["button_a"]
            and (
                (datetime.datetime.now() - self.button_a_input_time).total_seconds()
                >= INPUT_INTERVAL
            )
            and self.disp_mode != CLOCK_MODE
        ):
            self.init_clock_disp()
            self.disp_mode = CLOCK_MODE
            self.button_a_input_time = datetime.datetime.now()
        elif (
            data["button_b"]
            and (
                (datetime.datetime.now() - self.button_b_input_time).total_seconds()
                >= INPUT_INTERVAL
            )
            and self.disp_mode != SENSOR_MODE
        ):
            self.init_sensor_disp()
            self.disp_mode = SENSOR_MODE
            self.button_b_input_time = datetime.datetime.now()
        elif (
            data["button_c"]
            and (
                (datetime.datetime.now() - self.button_c_input_time).total_seconds()
                >= INPUT_INTERVAL
            )
            and self.disp_mode != IO_MODE
        ):
            self.init_io_disp()
            self.disp_mode = IO_MODE
            self.button_c_input_time = datetime.datetime.now()
        else:
            if self.disp_mode == CLOCK_MODE:
                self.update_clock_disp()
            elif self.disp_mode == SENSOR_MODE:
                self.update_sensor_disp()
            elif self.disp_mode == IO_MODE:
                self.update_io_disp()


def main() -> None:
    with AkariClient() as akari:
        m5_serial_sample = M5serialSample(akari.m5stack)
        while True:
            m5_serial_sample.display_update()
            time.sleep(0.01)


if __name__ == "__main__":
    main()
