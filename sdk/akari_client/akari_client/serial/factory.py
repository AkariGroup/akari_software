import contextlib
from typing import List

from ..config import (
    JointManagerDynamixelSerialConfig,
    JointManagerFeetechSerialConfig,
    M5StackSerialConfig,
)
from ..joint_manager import JointManager
from ..m5stack_client import M5StackClient
from .dynamixel import DynamixelController
from .dynamixel_communicator import DynamixelCommunicator
from .feetech import FeetechController
from .feetech_communicator import FeetechCommunicator
from .m5stack import M5StackSerialClient
from .m5stack_communicator import M5SerialCommunicator


def create_dynamixel_joint_manager(
    config: JointManagerDynamixelSerialConfig, stack: contextlib.ExitStack
) -> JointManager:
    communicator = stack.enter_context(
        DynamixelCommunicator.open(
            serial_port=config.serial_port,
            baudrate=config.baudrate,
            protocol_version=config.protocol_version,
        )
    )
    controllers: List[DynamixelController] = []
    for c in config.controllers:
        controllers.append(
            DynamixelController(
                c.joint_name,
                c.dynamixel_id,
                communicator,
            )
        )

    return JointManager(controllers)


def create_feetech_joint_manager(
    config: JointManagerFeetechSerialConfig, stack: contextlib.ExitStack
) -> JointManager:
    communicator = stack.enter_context(
        FeetechCommunicator.open(
            serial_port=config.serial_port,
            baudrate=config.baudrate,
        )
    )
    controllers: List[FeetechController] = []
    for c in config.controllers:
        controllers.append(
            FeetechController(
                c.joint_name,
                c.feetech_id,
                c.reverse,
                communicator,
            )
        )

    return JointManager(controllers)


def create_m5stack_client(
    config: M5StackSerialConfig, stack: contextlib.ExitStack
) -> M5StackClient:
    communicator = stack.enter_context(
        M5SerialCommunicator(
            baudrate=config.baudrate,
            port=config.serial_port,
            timeout=config.serial_timeout,
        )
    )
    return M5StackSerialClient(communicator)
