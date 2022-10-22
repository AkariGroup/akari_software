import abc


class RevoluteJointController(abc.ABC):
    @property
    @abc.abstractmethod
    def joint_name(self) -> str:
        ...

    @abc.abstractmethod
    def get_servo_enabled(self) -> bool:
        """サーボの有効無効状態を取得する。

        Returns:
            bool: サーボ有効なら``True``、無効なら``False``

        """
        ...

    @abc.abstractmethod
    def set_servo_enabled(self, enabled: bool) -> None:
        """サーボの有効無効状態を設定する。

        Args:
            enabled : ``True`` であればサーボを有効にする

        """
        ...

    @abc.abstractmethod
    def set_profile_acceleration(self, rad_per_sec2: float) -> None:
        """サーボの目標加速度を設定する。

        Args:
            rad_per_sec2: 加速度 [rad/s^2]

        """
        ...

    @abc.abstractmethod
    def set_profile_velocity(self, rad_per_sec: float) -> None:
        """サーボの目標速度を設定する。

        Args:
            rad_per_sec: 速度 [rad/s]

        """
        ...

    @abc.abstractmethod
    def set_goal_position(self, rad: float) -> None:
        """サーボの目標角度を設定する。
        ここで設定した値まで移動する。

        Args:
            rad: 目標角度 [rad]

        """
        ...

    @abc.abstractmethod
    def get_present_position(self) -> float:
        """サーボの現在角度を取得する。

        Returns:
            float: 現在角度 [rad]

        """
        ...
