from __future__ import annotations

import contextlib
import logging
from typing import Any, Optional

from .config import AkariClientConfig, load_config
from .joint_manager import JointManager
from .m5stack_client import M5StackClient


class AkariClient:
    def __init__(self, config: Optional[AkariClientConfig] = None) -> None:
        self._stack = contextlib.ExitStack()

        self._config = config or load_config()

        try:
            self._joints = self._config.joint_manager.factory(self._stack)
        except Exception:
            logging.warning(
                "Failed to boot joint manager. You can ignore this if you are not using joint control."
            )
            self._joints = None  # type: ignore

        try:
            self._m5stack = self._config.m5stack.factory(self._stack)
        except Exception:
            logging.warning(
                "Failed to boot m5stack. You can ignore this if you are not using m5stack."
            )
            self._m5stack = None  # type: ignore

    def __enter__(self) -> AkariClient:
        return self

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        self.close()

    def close(self) -> None:
        self._stack.close()

    @property
    def joints(self) -> JointManager:
        if self._joints is None:
            raise RuntimeError("JointManager is not connected")
        return self._joints

    @property
    def m5stack(self) -> M5StackClient:
        if self._m5stack is None:
            raise RuntimeError("M5Stack is not connected")
        return self._m5stack
