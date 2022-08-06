from __future__ import annotations

import contextlib
from typing import Any

from .joint_manager import JointManager
from .m5stack_client import M5StackClient, M5StackSerialClient


class AkariClient:
    def __init__(self) -> None:
        self._stack = contextlib.ExitStack()

        self._joints = self._stack.enter_context(JointManager())
        self._m5stack = self._stack.enter_context(M5StackSerialClient())

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
