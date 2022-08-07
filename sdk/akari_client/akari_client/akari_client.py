from __future__ import annotations

import contextlib
from typing import Any

from .joint_manager import JointManager
from .m5stack_client import M5StackClient
from .serial.dynamixel import create_controllers
from .serial.dynamixel_communicator import DynamixelCommunicator
from .serial.m5stack import M5StackSerialClient


def _initialize_joint_manager(
    stack: contextlib.ExitStack,
) -> JointManager:
    communicator = stack.enter_context(DynamixelCommunicator.open())
    controllers = create_controllers(communicator)
    return JointManager(controllers)


def _initialize_m5stack(stack: contextlib.ExitStack) -> M5StackClient:
    return stack.enter_context(M5StackSerialClient())


class AkariClient:
    def __init__(self) -> None:
        self._stack = contextlib.ExitStack()

        self._joints = _initialize_joint_manager(self._stack)
        self._m5stack = _initialize_m5stack(self._stack)

    def __enter__(self) -> AkariClient:
        return self

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        self.close()

    def close(self) -> None:
        self._stack.close()

    @property
    def joints(self) -> JointManager:
        return self._joints

    @property
    def m5stack(self) -> M5StackClient:
        return self._m5stack
