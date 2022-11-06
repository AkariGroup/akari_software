import abc
from typing import NamedTuple


class Limit(NamedTuple):
    min: float
    max: float


class RevoluteJointController(abc.ABC):
    @property
    @abc.abstractmethod
    def joint_name(self) -> str:
        ...

    @abc.abstractmethod
    def get_servo_enabled(self) -> bool:
        """サーボの有効無効状態を取得する。"""
        ...

    @abc.abstractmethod
    def set_servo_enabled(self, enabled: bool) -> None:
        """サーボの有効無効状態を設定する。

        Args:
            enabled: ``True`` であればサーボを有効にする

        """
        ...

    @abc.abstractmethod
    def get_position_limit(self) -> Limit:
        """Positionの上限値と下限値を取得する。

        Returns:
            現在角度の下限値、上限値 [rad]
        """
        ...

    @abc.abstractmethod
    def set_profile_acceleration(self, rad_per_sec2: float) -> None:
        """Profile Acceleration を設定する。

        Args:
            rad_per_sec2: 加速度 [rad/s^2]
        """
        ...

    @abc.abstractmethod
    def get_profile_acceleration(self) -> float:
        """Profile Acceleration を取得する。

        Retursn:
            加速度 [rad/s^2]
        """
        ...

    @abc.abstractmethod
    def set_profile_velocity(self, rad_per_sec: float) -> None:
        """Profile Velocity を設定する

        Args:
            rad_per_sec: 速度 [rad/s]
        """
        ...

    @abc.abstractmethod
    def get_profile_velocity(self) -> float:
        """Profile Velocity を設定する

        Args:
            rad_per_sec: 速度 [rad/s]
        """
        ...

    @abc.abstractmethod
    def set_goal_position(self, rad: float) -> None:
        """目標角度を設定する。

        Args:
            rad: 目標角度 [rad]
        """
        ...

    @abc.abstractmethod
    def get_present_position(self) -> float:
        """現在角度を取得する

        Returns:
            現在角度 [rad]
        """
        ...

    @abc.abstractmethod
    def get_moving_state(self) -> bool:
        """モーターが動作中かどうか判定する。

        Returns:
            現在のモーター状態。
        """
        ...
