from __future__ import annotations

import contextlib
from typing import Any, Optional

from .config import AkariClientConfig, load_config
from .joint_manager import JointManager
from .m5stack_client import M5StackClient


class AkariClient:
    def __init__(self, config: Optional[AkariClientConfig] = None) -> None:
        self._stack = contextlib.ExitStack()

        self._config = config or load_config()
        self._joints = self._config.joint_manager.factory(self._stack)
        self._m5stack = self._config.m5stack.factory(self._stack)

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
