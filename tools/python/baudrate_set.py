#!/usr/bin/env python
# -*- coding: utf-8 -*-

from akari_client.serial.dynamixel import DynamixelControlTable
from akari_client.serial.dynamixel_communicator import (
    DynamixelCommunicator,
    get_baudrate_control_value,
)

_BAUDRATES = [9600, 57600, 115200, 1000000, 2000000, 3000000, 4000000, 4500000]

TARGET_BAUDRATE = 1000000


def main() -> None:
    for cur in _BAUDRATES:
        print("Scan:" + str(cur))
        try:
            with DynamixelCommunicator.open(baudrate=cur) as comm:
                control = DynamixelControlTable.TORQUE_ENABLE
                comm.write(2, control.address, control.length, False)
                control = DynamixelControlTable.BAUD_RATE
                baudrate_entry = get_baudrate_control_value(TARGET_BAUDRATE)
                comm.write(1, control.address, control.length, baudrate_entry)
                print("Successfuly set baudrate to " + str(TARGET_BAUDRATE))
                return
        except RuntimeError:
            pass
    print("Dynamixel not found")


if __name__ == "__main__":
    main()
