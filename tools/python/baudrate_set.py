#!/usr/bin/env python
# -*- coding: utf-8 -*-

from akari_client.dynamixel_communicator import (
    DynamixelCommunicator,
    get_baudrate_control_value,
)
from akari_client.dynamixel_controller import DynamixelControlTable

# Note: you can choose 57600 or 1000000 as a baud rate value for now.
CURRENT_BAUDRATE = 57600
TARGET_BAUDRATE = 1000000


with DynamixelCommunicator.open(baudrate=CURRENT_BAUDRATE) as comm:
    control = DynamixelControlTable.BAUD_RATE
    baudrate_entry = get_baudrate_control_value(TARGET_BAUDRATE)
    comm.write(1, control.address, control.length, baudrate_entry)
    print("Successfuly set baudrate")
