import dataclasses
import math

from ..joint_controller import PositionLimit, RevoluteJointController
from .dynamixel_communicator import DynamixelCommunicator

PULSE_OFFSET = 2047


def dynamixel_pulse_to_rad(data: int) -> float:
    """dynamixelのpulse単位をラジアン単位に変換する。"""
    return (data - PULSE_OFFSET) * (2 * math.pi) / 4095


def rad_to_dynamixel_pulse(data: float) -> int:
    """ラジアン単位をdynamixelのpulse単位に変換する。"""
    return int(data * 4095 / (2 * math.pi)) + PULSE_OFFSET


def rad_per_sec2_to_rev_per_min2(data: float) -> int:
    """加速度を rad/s^2 単位 から rev/m^2 単位に変換する。"""
    return int(data * 60 * 60 / (2 * math.pi))


def rev_per_min2_to_rad_per_sec2(data: int) -> float:
    """加速度を rev/m^2 単位 から rad/s^2 単位に変換する。"""
    return float(data * (2 * math.pi) / (60 * 60))


def rad_per_sec_to_rev_per_min(data: float) -> int:
    """速度を rad/s 単位 から rpm 単位に変換する。"""
    return int(data * 60 / (2 * math.pi))


def rev_per_min_to_rad_per_sec(data: int) -> float:
    """速度を rpm 単位 から rad/s 単位に変換する。"""
    return float(data * (2 * math.pi) / 60)


@dataclasses.dataclass(frozen=True)
class DynamixelControlItem:
    data_name: str
    address: int
    length: int


class DynamixelControlTable:
    ID = DynamixelControlItem("ID", 7, 1)
    BAUD_RATE = DynamixelControlItem("Baud_Rate", 8, 1)
    DRIVE_MODE = DynamixelControlItem("Drive_Mode", 10, 1)
    MAX_POSITION_LIMIT = DynamixelControlItem("Max_Position_Limit", 48, 4)
    MIN_POSITION_LIMIT = DynamixelControlItem("Min_Position_Limit", 52, 4)
    TORQUE_ENABLE = DynamixelControlItem("Torque_Enable", 64, 1)
    PROFILE_ACCELERATION = DynamixelControlItem("Profile_Acceleration", 108, 4)
    PROFILE_VELOCITY = DynamixelControlItem("Profile_Velocity", 112, 4)
    GOAL_POSITION = DynamixelControlItem("Goal_Position", 116, 4)
    PRESENT_POSITION = DynamixelControlItem("Present_Position", 132, 4)
    MOVING_STATUS = DynamixelControlItem("Moving_Status", 123, 1)


class DynamixelController(RevoluteJointController):
    def __init__(
        self,
        joint_name: str,
        dynamixel_id: int,
        communicator: DynamixelCommunicator,
    ) -> None:
        """
        dynamixelのコントローラ。

        Args:
            communicator: dynamixel通信用クラス

        """
        self._joint_name = joint_name
        self._dynamixel_id = dynamixel_id
        self._communicator = communicator

    def __str__(self) -> str:
        return self._joint_name

    def _read(self, item: DynamixelControlItem) -> int:
        return self._communicator.read(self._dynamixel_id, item.address, item.length)

    def _write(self, item: DynamixelControlItem, value: int) -> None:
        self._communicator.write(self._dynamixel_id, item.address, item.length, value)

    def set_position_limit(self, lower_rad: float, upper_rad: float) -> None:
        """Positionの上限値と下限値を設定する。

        Args:
            lower_rad: 下限値 [rad]
            upper_rad: 上限値 [rad]

        """
        self._write(
            DynamixelControlTable.MIN_POSITION_LIMIT, rad_to_dynamixel_pulse(lower_rad)
        )
        self._write(
            DynamixelControlTable.MAX_POSITION_LIMIT, rad_to_dynamixel_pulse(upper_rad)
        )

    def get_position_limit(self) -> PositionLimit:
        """Positionの上限値と下限値を取得する。

        Returns:
            現在角度の下限値、上限値 [rad]

        """
        min = dynamixel_pulse_to_rad(
            self._read(DynamixelControlTable.MIN_POSITION_LIMIT)
        )
        max = dynamixel_pulse_to_rad(
            self._read(DynamixelControlTable.MAX_POSITION_LIMIT)
        )
        return PositionLimit(min, max)

    @property
    def joint_name(self) -> str:
        """関節名を取得する。

        Returns:
           関節名

        """
        return self._joint_name

    def get_servo_enabled(self) -> bool:
        """サーボの有効無効状態を取得する。"""
        return self._read(DynamixelControlTable.TORQUE_ENABLE) == 1

    def set_servo_enabled(self, enabled: bool) -> None:
        """サーボの有効無効状態を設定する。

        Args:
            enabled: Trueであればサーボを有効にする

        """
        self._write(DynamixelControlTable.TORQUE_ENABLE, int(enabled))

    def set_profile_acceleration(self, rad_per_sec2: float) -> None:
        """Profile Acceleration を設定する。

        Args:
            rad_per_sec2: 加速度 [rad/s^2]

        """
        self._write(
            DynamixelControlTable.PROFILE_ACCELERATION,
            rad_per_sec2_to_rev_per_min2(rad_per_sec2),
        )

    def get_profile_acceleration(self) -> float:
        """Profile Acceleration を取得する。

        Returns:
            加速度 [rad/s^2]

        """
        return rev_per_min2_to_rad_per_sec2(
            self._read(DynamixelControlTable.PROFILE_ACCELERATION)
        )

    def set_profile_velocity(self, rad_per_sec: float) -> None:
        """Profile Velocity を設定する。

        Args:
            rad_per_sec: 速度 [rad/s]

        """
        self._write(
            DynamixelControlTable.PROFILE_VELOCITY,
            rad_per_sec_to_rev_per_min(rad_per_sec),
        )

    def get_profile_velocity(self) -> float:
        """Profile Velocity を取得する。

        Returns:
            加速度 [rad/s^2]

        """
        return rev_per_min_to_rad_per_sec(
            self._read(DynamixelControlTable.PROFILE_VELOCITY)
        )

    def set_goal_position(self, rad: float) -> None:
        """サーボの目標角度を設定する。

        Args:
            rad: 目標角度 [rad]

        """
        self._write(DynamixelControlTable.GOAL_POSITION, rad_to_dynamixel_pulse(rad))

    def get_present_position(self) -> float:
        """サーボの現在角度を取得する。

        Returns:
            現在角度 [rad]

        """
        return dynamixel_pulse_to_rad(
            self._read(DynamixelControlTable.PRESENT_POSITION)
        )

    def get_moving_state(self) -> bool:
        """サーボが動作中かどうか判定する。

        Returns:
            現在のサーボ状態

        """
        val = bin(self._read(DynamixelControlTable.MOVING_STATUS))
        if len(val) < 7:
            return True
        elif int(bin(self._read(DynamixelControlTable.MOVING_STATUS))[-2]) < 1:
            return True
        return False
