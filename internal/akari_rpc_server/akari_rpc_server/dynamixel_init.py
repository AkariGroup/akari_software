import logging
from typing import Sequence

from akari_client.config import JointManagerDynamixelSerialConfig
from akari_client.serial import dynamixel_communicator
from akari_client.serial.dynamixel import (
    DynamixelCommunicator,
    DynamixelController,
    DynamixelControlTable,
)

_logger = logging.getLogger(__name__)
BAUDRATE_GUESSES = [9600, 57600, 115200, 1000000, 2000000, 3000000, 4000000, 4500000]


def initialize_baudrate(config: JointManagerDynamixelSerialConfig) -> None:
    dynamixel_ids = [c.dynamixel_id for c in config.controllers]
    baudrate_entry = dynamixel_communicator.get_baudrate_control_value(config.baudrate)

    for guess in [config.baudrate] + BAUDRATE_GUESSES:
        try:
            with DynamixelCommunicator.open(baudrate=guess) as comm:
                control = DynamixelControlTable.TORQUE_ENABLE
                for id in dynamixel_ids:
                    comm.write(id, control.address, control.length, False)

                control = DynamixelControlTable.BAUD_RATE
                comm.write(1, control.address, control.length, baudrate_entry)
                _logger.info(
                    f"Successfuly set baudrate to {dynamixel_communicator.DEFAULT_BAUDRATE}"
                )
                return
        except RuntimeError:
            pass


def initialize_joint_limit(
    controllers: Sequence[DynamixelController],
    dynamixel_config: JointManagerDynamixelSerialConfig,
) -> None:
    for config in dynamixel_config.controllers:
        controller = next(
            (c for c in controllers if c.joint_name == config.joint_name), None
        )
        if controller is None:
            _logger.warning(f"Joint: '{config.joint_name}' doesn't exist")
            continue

        controller.set_servo_enabled(False)
        controller.set_position_limit(
            config.min_position_limit, config.max_position_limit
        )
        _logger.info(f"Successfully set position limit of joint: '{config.joint_name}'")


def initialize_default_velocity(
    controllers: Sequence[DynamixelController],
    dynamixel_config: JointManagerDynamixelSerialConfig,
) -> None:
    for config in dynamixel_config.controllers:
        controller = next(
            (c for c in controllers if c.joint_name == config.joint_name), None
        )
        if controller is None:
            _logger.warning(f"Joint: '{config.joint_name}' doesn't exist")
            continue
        controller.set_profile_velocity(config.default_velocity)
        _logger.info(f"Successfully set velocity of joint: '{config.joint_name}'")


def initialize_default_acceleration(
    controllers: Sequence[DynamixelController],
    dynamixel_config: JointManagerDynamixelSerialConfig,
) -> None:
    for config in dynamixel_config.controllers:
        controller = next(
            (c for c in controllers if c.joint_name == config.joint_name), None
        )
        if controller is None:
            _logger.warning(f"Joint: '{config.joint_name}' doesn't exist")
            continue
        controller.set_profile_acceleration(config.default_acceleration)
        _logger.info(f"Successfully set acceleration of joint: '{config.joint_name}'")
