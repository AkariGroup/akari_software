from __future__ import annotations

import enum
import time
from typing import Dict, Iterator, List, Optional, Sequence, Tuple, TypeVar

from .joint_controller import PositionLimit, RevoluteJointController

TValue = TypeVar("TValue")


class AkariJoint(str, enum.Enum):
    """
    AKARIの関節名の一覧。
    """

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
        """関節名を取得する。

        Returns:
            AKARIの全関節名のlist

        """
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

    def get_joint_limits(self) -> Dict[str, PositionLimit]:
        """サーボの位置リミットを取得する。

        Returns:
            関節名と位置リミット(min,max)[rad]のDict

        Example:
            >>> from akari_client import AkariClient
            >>> akari = AkariClient()
            >>> joints = akari.joints
            >>> print(joints.get_joint_limits())
            # 各軸のリミット値が出力される

        """
        ret: Dict[str, PositionLimit] = {}
        for joint_name, controller in self._joints.items():
            ret[joint_name] = controller.get_position_limit()
        return ret

    def set_joint_accelerations(
        self,
        *,
        pan: Optional[float] = None,
        tilt: Optional[float] = None,
        **kwargs: float,
    ) -> None:
        """サーボの目標加速度を設定する。

        Args:
            pan: pan軸の加速度 [rad/s^2]
            tilt: tilt軸の加速度 [rad/s^2]

        Example:
            >>> from akari_client import AkariClient
            >>> akari = AkariClient()
            >>> joints = akari.joints
            >>> joints.set_joint_accelerations(pan=10, tilt=8)
            # pan軸の目標加速度が10rad/s^2, tilt軸の目標加速度が8rad/s^2

        """
        for joint, value in self._iter_joint_value_pairs(pan, tilt, **kwargs):
            joint.set_profile_acceleration(value)

    def get_joint_accelerations(self) -> Dict[str, float]:
        """サーボの目標加速度を取得する。

        Returns:
            関節名と目標加速度[rad/s^2]のDict

        Example:
            >>> from akari_client import AkariClient
            >>> akari = AkariClient()
            >>> joints = akari.joints
            >>> print(joints.get_joint_accelerations())
            # 各軸の目標加速度値が出力される

        """
        ret: Dict[str, float] = {}
        for joint_name, controller in self._joints.items():
            ret[joint_name] = controller.get_profile_acceleration()
        return ret

    def set_joint_velocities(
        self,
        *,
        pan: Optional[float] = None,
        tilt: Optional[float] = None,
        **kwargs: float,
    ) -> None:
        """サーボの目標速度を設定する。

        Args:
            pan: pan軸の速度 [rad/s]
            tilt: tilt軸の速度 [rad/s]

        Example:
            >>> from akari_client import AkariClient
            >>> akari = AkariClient()
            >>> joints = akari.joints
            >>> joints.set_joint_velocities(pan=10, tilt=8)
            # pan軸の目標加速度が10rad/s, tilt軸の目標加速度が8rad/s

        """
        for joint, value in self._iter_joint_value_pairs(pan, tilt, **kwargs):
            joint.set_profile_velocity(value)

    def get_joint_velocities(self) -> Dict[str, float]:
        """サーボの目標速度を取得する。

        Returns:
            関節名と目標速度[rad/s]のDict

        Example:
            >>> from akari_client import AkariClient
            >>> akari = AkariClient()
            >>> joints = akari.joints
            >>> print(joints.get_joint_velocities())
            # 各軸の目標速度値が出力される

        """
        ret: Dict[str, float] = {}
        for joint_name, controller in self._joints.items():
            ret[joint_name] = controller.get_profile_velocity()
        return ret

    def move_joint_positions(
        self,
        *,
        sync: bool = False,
        pan: Optional[float] = None,
        tilt: Optional[float] = None,
        **kwargs: float,
    ) -> None:
        """サーボの目標角度を設定する。
        ここで設定した値まで移動する。

        Args:
            sync: Trueにすると、サーボの移動が完了するまで関数の終了を待機する。デフォルト値はFalse。
            pan: pan軸の目標角度 [rad]
            tilt: tilt軸の目標角度 [rad]

        Example:
            >>> from akari_client import AkariClient
            >>> akari = AkariClient()
            >>> joints = akari.joints
            >>> joints.move_joint_positions(pan=0.4,tilt=-0.2)
            # pan軸が0.4rad, tilt軸の目標加速度が-0.2radの位置へ移動

        """
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
        """サーボの現在角度を取得する。

        Returns:
            サーボ名と現在角度[rad]のdict

        Example:
            >>> from akari_client import AkariClient
            >>> akari = AkariClient()
            >>> joints = akari.joints
            >>> print(joints.get_joint_positions())
            # 各軸の現在角度[rad]が出力される

        """
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
        """サーボの有効無効状態を設定する。

        Args:
            pan: pan軸のサーボ有効無効の設定。``True`` であればサーボを有効にする。
            tilt: tilt軸のサーボ有効無効の設定。``True`` であればサーボを有効にする。

        Example:
            >>> from akari_client import AkariClient
            >>> akari = AkariClient()
            >>> joints = akari.joints
            >>> joints.set_servo_enabled(pan=True,tilt=False)
            # panのサーボを有効、tiltのサーボを無効に設定

        """
        for joint, value in self._iter_joint_value_pairs(pan, tilt, **kwargs):
            joint.set_servo_enabled(value)

    def enable_all_servo(self) -> None:
        """全サーボを有効状態に設定する。

        Example:
            >>> from akari_client import AkariClient
            >>> akari = AkariClient()
            >>> joints = akari.joints
            >>> joints.enable_all_servo()
            # pan、tiltのサーボ両方を有効に設定

        """
        for joint in self._joints.values():
            joint.set_servo_enabled(True)

    def disable_all_servo(self) -> None:
        """全サーボを無効状態に設定する。

        Example:
            >>> from akari_client import AkariClient
            >>> akari = AkariClient()
            >>> joints = akari.joints
            >>> joints.disable_all_servo()
            # pan、tiltのサーボ両方を無効に設定

        """
        for joint in self._joints.values():
            joint.set_servo_enabled(False)

    def get_moving_state(self) -> Dict[str, bool]:
        """サーボが現在移動中かを取得する。
            停止中ならTrue、移動中ならFalseを返す。

        Returns:
            サーボ名と現在状態のdict

        Example:
            >>> from akari_client import AkariClient
            >>> akari = AkariClient()
            >>> joints = akari.joints
            >>> print(joints.get_moving_state())
            # 各軸の現在状態が出力される

        """
        ret: Dict[str, bool] = {}
        for joint_name, controller in self._joints.items():
            ret[joint_name] = controller.get_moving_state()

        return ret
