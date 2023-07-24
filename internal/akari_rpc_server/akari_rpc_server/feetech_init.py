import logging
from typing import Sequence

from akari_client.config import JointManagerFeetechSerialConfig
from akari_client.serial import feetech_communicator
from akari_client.serial.feetech import (
    FeetechCommunicator,
    FeetechController,
    FeetechControlTable,
)

_logger = logging.getLogger(__name__)
BAUDRATE_GUESSES = [9600, 57600, 115200, 1000000, 2000000, 3000000, 4000000, 4500000]


def initialize_baudrate(config: JointManagerFeetechSerialConfig) -> None:
    feetech_ids = [c.feetech_id for c in config.controllers]
    baudrate_entry = feetech_communicator.get_baudrate_control_value(config.baudrate)

    for guess in [config.baudrate] + BAUDRATE_GUESSES:
        try:
            with FeetechCommunicator.open(baudrate=guess) as comm:
                control = FeetechControlTable.TORQUE_ENABLE
                for id in feetech_ids:
                    comm.write(id, control.address, control.length, False)

                control = FeetechControlTable.BAUD_RATE
                comm.write(1, control.address, control.length, baudrate_entry)
                _logger.info(
                    f"Successfuly set baudrate to {feetech_communicator.DEFAULT_BAUDRATE}"
                )
                return
        except RuntimeError:
            pass


def initialize_joint_limit(
    controllers: Sequence[FeetechController],
    feetech_config: JointManagerFeetechSerialConfig,
) -> None:
    for config in feetech_config.controllers:
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
    controllers: Sequence[FeetechController],
    feetech_config: JointManagerFeetechSerialConfig,
) -> None:
    for config in feetech_config.controllers:
        controller = next(
            (c for c in controllers if c.joint_name == config.joint_name), None
        )
        if controller is None:
            _logger.warning(f"Joint: '{config.joint_name}' doesn't exist")
            continue
        controller.set_profile_velocity(config.default_velocity)
        _logger.info(f"Successfully set velocity of joint: '{config.joint_name}'")


def initialize_default_acceleration(
    controllers: Sequence[FeetechController],
    feetech_config: JointManagerFeetechSerialConfig,
) -> None:
    for config in feetech_config.controllers:
        controller = next(
            (c for c in controllers if c.joint_name == config.joint_name), None
        )
        if controller is None:
            _logger.warning(f"Joint: '{config.joint_name}' doesn't exist")
            continue
        controller.set_profile_acceleration(config.default_acceleration)
        _logger.info(f"Successfully set acceleration of joint: '{config.joint_name}'")
