#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
m5_reset.py
Created on 2021/09/20
@author: Kazuya Yamamoto

M5をハードリセットして再起動するツール
実行後は下記コマンドでAKARIの自動起動サービスを再起動すること
ROS2: sudo systemctl restart auto_start_ros.service
非ROS: sudo systemctl restart auto_start.service
"""

import time

import serial

BAUDRATE = 500000
DEVICE_NAME = "/dev/ttyUSB_M5Stack"
TIMEOUT = 0.2


def main() -> None:
    ser = serial.Serial(baudrate=BAUDRATE, port=DEVICE_NAME, timeout=TIMEOUT)
    ser.setDTR(False)
    time.sleep(0.1)
    ser.setRTS(False)
    ser.rtscts = False
    time.sleep(1)
    ser.close()


if __name__ == "__main__":
    main()
