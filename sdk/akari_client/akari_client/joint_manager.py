from __future__ import annotations

import enum
import time
from typing import Dict, Iterator, List, Optional, Sequence, Tuple, TypeVar

from .joint_controller import RevoluteJointController

TValue = TypeVar("TValue")


class AkariJoint(str, enum.Enum):
    PAN = "pan"
    TILT = "tilt"


class JointManager:
    def __init__(self, joint_controllers: Sequence[RevoluteJointController]) -> None:
        """Akariの関節制御コントローラ"""

        self._joints: Dict[str, RevoluteJointController] = {}
        for j in joint_controllers:
            self._joints[j.joint_name] = j

    @property
    def joint_controllers(self) -> Sequence[RevoluteJointController]:
        return list(self._joints.values())

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
        sync: bool = False,
        pan: Optional[float] = None,
        tilt: Optional[float] = None,
        **kwargs: float,
    ) -> None:
        for joint, position in self._iter_joint_value_pairs(pan, tilt, **kwargs):
            joint.set_goal_position(position)
        if sync:
            while True:
                for joint, position in self._iter_joint_value_pairs(
                    pan, tilt, **kwargs
                ):
                    if not joint.get_moving_state():
                        break
                else:
                    break
                time.sleep(0.01)

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
