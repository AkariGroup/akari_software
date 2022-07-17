from __future__ import annotations

import contextlib
import enum
from typing import Any, Dict, Iterator, List, Optional, Tuple, TypeVar

from .dynamixel_communicator import DynamixelCommunicator
from .dynamixel_controller import DynamixelController, DynamixelControllerConfig
from .joint_controller import RevoluteJointController

TValue = TypeVar("TValue")


class AkariJoint(str, enum.Enum):
    PAN = "pan"
    TILT = "tilt"


DEFAULT_JOINT_CONFIGS: List[DynamixelControllerConfig] = [
    DynamixelControllerConfig(
        joint_name=AkariJoint.PAN,
        dynamixel_id=1,
        min_position_limit=-2.355,
        max_position_limit=2.355,
    ),
    DynamixelControllerConfig(
        joint_name=AkariJoint.TILT,
        dynamixel_id=2,
        min_position_limit=-0.91,
        max_position_limit=0.91,
    ),
]


class JointManager:
    def __init__(self, communicator: Optional[DynamixelCommunicator] = None) -> None:
        """Akariの関節制御コントローラ"""

        self._stack = contextlib.ExitStack()
        if communicator is None:
            self._communicator = self._stack.enter_context(DynamixelCommunicator.open())
        else:
            self._communicator = communicator

        self._joints: Dict[str, RevoluteJointController] = {}
        for config in DEFAULT_JOINT_CONFIGS:
            # TODO: Dispatch ControllerInitialization by a config class
            assert isinstance(config, DynamixelControllerConfig)
            self._joints[config.joint_name] = DynamixelController(
                config,
                self._communicator,
            )

    def __enter__(self) -> JointManager:
        return self

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        self.close()

    def close(self) -> None:
        self._stack.close()

    def get_joint_names(self) -> List[str]:
        """関節名を取得する。"""
        return list(self._joints.keys())

    @property
    def pan_joint(self) -> RevoluteJointController:
        return self._joints[AkariJoint.PAN]

    @property
    def tilt_joint(self) -> RevoluteJointController:
        return self._joints[AkariJoint.TILT]

    def _iter_joint_value_pairs(
        self,
        pan: Optional[TValue] = None,
        tilt: Optional[TValue] = None,
        **kwargs: TValue,
    ) -> Iterator[Tuple[RevoluteJointController, TValue]]:
        values: Dict[str, TValue] = {}
        if pan is not None:
            values[AkariJoint.PAN] = pan
        if tilt is not None:
            values[AkariJoint.TILT] = tilt
        values.update(kwargs)

        for joint_name, value in values.items():
            controller = self._joints[joint_name]
            yield controller, value

    def set_joint_accelerations(
        self,
        *,
        pan: Optional[float] = None,
        tilt: Optional[float] = None,
        **kwargs: float,
    ) -> None:
        for joint, value in self._iter_joint_value_pairs(pan, tilt, **kwargs):
            joint.set_profile_acceleration(value)

    def set_joint_velocities(
        self,
        *,
        pan: Optional[float] = None,
        tilt: Optional[float] = None,
        **kwargs: float,
    ) -> None:
        for joint, value in self._iter_joint_value_pairs(pan, tilt, **kwargs):
            joint.set_profile_velocity(value)

    def move_joint_positions(
        self,
        *,
        pan: Optional[float] = None,
        tilt: Optional[float] = None,
        **kwargs: float,
    ) -> None:
        for joint, position in self._iter_joint_value_pairs(pan, tilt, **kwargs):
            joint.set_goal_position(position)

    def get_joint_positions(self) -> Dict[str, float]:
        ret: Dict[str, float] = {}
        for joint_name, controller in self._joints.items():
            ret[joint_name] = controller.get_present_position()

        return ret

    def set_servo_enabled(
        self,
        *,
        pan: Optional[bool] = None,
        tilt: Optional[bool] = None,
        **kwargs: bool,
    ) -> None:
        for joint, value in self._iter_joint_value_pairs(pan, tilt, **kwargs):
            joint.set_servo_enabled(value)

    def enable_all_servo(self) -> None:
        for joint in self._joints.values():
            joint.set_servo_enabled(True)

    def disable_all_servo(self) -> None:
        for joint in self._joints.values():
            joint.set_servo_enabled(False)
