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

from akari_controller.m5serial_server_py import M5SerialServer

CLOCK_MODE = 1
SENSOR_MODE = 2
IO_MODE = 3
duration = 0.01
INPUT_INTERVAL = 1  # ボタン再入力受付時間[s]
m5 = M5SerialServer()


class M5serialSample(object):
    def __init__(self) -> None:
        # global m5
        # m5 = M5SerialServer()
        self.is_initializing = False
        self.button_a_input_time = datetime.datetime.now()
        self.button_b_input_time = datetime.datetime.now()
        self.button_c_input_time = datetime.datetime.now()
        self.disp_mode = 0
        # m5.reset_m5()

    def init_clock_disp(self) -> None:
        global duration
        duration = 0.5
        m5.set_display_color("black")
        locale.setlocale(locale.LC_TIME, "ja_JP.UTF-8")
        dt_now = datetime.datetime.now()
        m5.set_display_text(
            dt_now.strftime("%Y/%m/%d %a"),
            -999,
            0,
            2,
            "white",
            "black",
            True,
        )
        self.is_initializing = False

    def update_clock_disp(self) -> None:
        if self.disp_mode == CLOCK_MODE:
            dt_now = datetime.datetime.now()
            m5.set_display_text(
                dt_now.strftime("%H:%M:%S "),
                -999,
                -999,
                4,
                "white",
                "black",
                False,
            )

    def init_sensor_disp(self) -> None:
        m5.set_display_color("lightgrey")
        self.is_initializing = False

    def update_sensor_disp(self) -> None:
        if self.disp_mode == SENSOR_MODE:
            m5.set_display_text(
                "明るさ: " + str(self.brightness).rjust(4, " ") + " \n",
                0,
                20,
                2,
                "orange",
                "",
                False,
            )
        if self.disp_mode == SENSOR_MODE:
            m5.set_display_text(
                "気圧: " + str(round(self.pressure / 100, 2)).rjust(7, " ") + " hPa  \n",
                0,
                100,
                2,
                "pink",
                "",
                False,
            )
        if self.disp_mode == SENSOR_MODE:
            m5.set_display_text(
                "気温: " + str(round(self.temperature, 2)).rjust(7, " ") + " C \n",
                0,
                180,
                2,
                "purple",
                "",
                False,
            )

    def init_io_disp(self) -> None:
        m5.set_display_color("white")
        self.is_initializing = False

    def update_io_disp(self) -> None:
        if self.disp_mode == IO_MODE:
            if self.din0:
                m5.set_display_text(
                    "din0: " + str(int(self.din0)) + " \n",
                    0,
                    0,
                    2,
                    "white",
                    "red",
                    False,
                )
            else:
                m5.set_display_text(
                    "din0: " + str(int(self.din0)) + "    \n",
                    0,
                    0,
                    2,
                    "black",
                    "",
                    False,
                )
        if self.disp_mode == IO_MODE:
            if self.din1:
                m5.set_display_text(
                    "din1: " + str(int(self.din1)) + " \n",
                    0,
                    40,
                    2,
                    "white",
                    "red",
                    False,
                )
            else:
                m5.set_display_text(
                    "din1: " + str(int(self.din1)) + "    \n",
                    0,
                    40,
                    2,
                    "black",
                    "",
                    False,
                )
        if self.disp_mode == IO_MODE:
            if self.ain0 > 0:
                m5.set_display_text(
                    "ain0: " + str(int(self.ain0)).rjust(3, " ") + " \n",
                    0,
                    80,
                    2,
                    "white",
                    "green",
                    False,
                )
            else:
                m5.set_display_text(
                    "ain0: " + str(int(self.ain0)).rjust(3, " ") + "    \n",
                    0,
                    80,
                    2,
                    "green",
                    "",
                    False,
                )
        if self.disp_mode == IO_MODE:
            if self.dout0:
                m5.set_display_text(
                    "dout0: " + str(int(self.dout0)) + " \n",
                    0,
                    120,
                    2,
                    "white",
                    "red",
                    False,
                )
            else:
                m5.set_display_text(
                    "dout0: " + str(int(self.dout0)) + "    \n",
                    0,
                    120,
                    2,
                    "black",
                    "",
                    False,
                )
        if self.disp_mode == IO_MODE:
            if self.dout1:
                m5.set_display_text(
                    "dout1: " + str(int(self.dout1)) + " \n",
                    0,
                    160,
                    2,
                    "white",
                    "red",
                    False,
                )
            else:
                m5.set_display_text(
                    "dout1: " + str(int(self.dout1)) + "    \n",
                    0,
                    160,
                    2,
                    "black",
                    "",
                    False,
                )
        if self.disp_mode == IO_MODE:
            if self.pwmout0 > 0:
                m5.set_display_text(
                    "pwmout0: " + str(int(self.pwmout0)).rjust(3, " ") + " \n",
                    0,
                    200,
                    2,
                    "white",
                    "blue",
                    False,
                )
            else:
                m5.set_display_text(
                    "pwmout0: " + str(int(self.pwmout0)).rjust(3, " ") + "    \n",
                    0,
                    200,
                    2,
                    "blue",
                    "",
                    False,
                )

    def display_update(self) -> None:
        data = m5.get()
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
    m5_serial_sample = M5serialSample()
    while True:
        m5_serial_sample.display_update()
        time.sleep(0.01)


if __name__ == "__main__":
    main()
