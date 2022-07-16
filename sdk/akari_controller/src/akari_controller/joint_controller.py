import abc
import dataclasses


@dataclasses.dataclass(frozen=True)
class JointControllerConfig:
    joint_name: str


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
    def set_profile_acceleration(self, rad_per_sec2: float) -> None:
        """Profile Acceleration を設定する。

        Args:
            rad_per_sec2: 加速度 [rad/s^2]
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