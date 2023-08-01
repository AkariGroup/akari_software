import dataclasses
import math

from ..joint_controller import PositionLimit, RevoluteJointController
from .feetech_communicator import FeetechCommunicator

PULSE_OFFSET = 2047


def feetech_pulse_to_rad(data: int) -> float:
    """feetechのpulse単位をラジアン単位に変換する。"""
    return ( -1 * (data - PULSE_OFFSET)) * (2 * math.pi) / 4095


def rad_to_feetech_pulse(data: float) -> int:
    """ラジアン単位をfeetechのpulse単位に変換する。"""
    return int(-1 * data * 4095 / (2 * math.pi)) + PULSE_OFFSET


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
class FeetechControlItem:
    data_name: str
    address: int
    length: int


class FeetechControlTable:
    ID = FeetechControlItem("ID", 5, 1)
    BAUD_RATE = FeetechControlItem("Baud_Rate", 6, 1)
    EEPROM_LOCK = FeetechControlItem("Eeprom_lock", 55, 1)
    MAX_POSITION_LIMIT = FeetechControlItem("Max_Position_Limit", 9, 2)
    MIN_POSITION_LIMIT = FeetechControlItem("Min_Position_Limit", 11, 2)
    TORQUE_ENABLE = FeetechControlItem("Torque_Enable", 40, 1)
    PROFILE_ACCELERATION = FeetechControlItem("Profile_Acceleration", 41, 1)
    PROFILE_VELOCITY = FeetechControlItem("Profile_Velocity", 46, 2)
    GOAL_POSITION = FeetechControlItem("Goal_Position", 42, 2)
    PRESENT_POSITION = FeetechControlItem("Present_Position", 56, 2)
    MOVING_STATUS = FeetechControlItem("Moving_Status",66, 1)


class FeetechController(RevoluteJointController):
    def __init__(
        self,
        joint_name: str,
        feetech_id: int,
        communicator: FeetechCommunicator,
    ) -> None:
        """
        feetechのコントローラ。

        Args:
            communicator: feetech通信用クラス

        """
        self._joint_name = joint_name
        self._feetech_id = feetech_id
        self._communicator = communicator

    def __str__(self) -> str:
        return self._joint_name

    def _read(self, item: FeetechControlItem) -> int:
        return self._communicator.read(self._feetech_id, item.address, item.length)

    def _write(self, item: FeetechControlItem, value: int) -> None:
        self._communicator.write(self._feetech_id, item.address, item.length, value)

    def set_position_limit(self, lower_rad: float, upper_rad: float) -> None:
        """Positionの上限値と下限値を設定する。

        Args:
            lower_rad: 下限値 [rad]
            upper_rad: 上限値 [rad]

        """
        self._write(
            FeetechControlTable.EEPROM_LOCK, 0
        )
        self._write(
            FeetechControlTable.MIN_POSITION_LIMIT, rad_to_feetech_pulse(lower_rad)
        )
        self._write(
            FeetechControlTable.MAX_POSITION_LIMIT, rad_to_feetech_pulse(upper_rad)
        )
        self._write(
            FeetechControlTable.EEPROM_LOCK, 1
        )

    def get_position_limit(self) -> PositionLimit:
        """Positionの上限値と下限値を取得する。

        Returns:
            現在角度の下限値、上限値 [rad]

        """
        min = feetech_pulse_to_rad(
            self._read(FeetechControlTable.MIN_POSITION_LIMIT)
        )
        max = feetech_pulse_to_rad(
            self._read(FeetechControlTable.MAX_POSITION_LIMIT)
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
        return self._read(FeetechControlTable.TORQUE_ENABLE) == 1

    def set_servo_enabled(self, enabled: bool) -> None:
        """サーボの有効無効状態を設定する。

        Args:
            enabled: Trueであればサーボを有効にする

        """
        self._write(FeetechControlTable.TORQUE_ENABLE, int(enabled))

    def set_profile_acceleration(self, rad_per_sec2: float) -> None:
        """Profile Acceleration を設定する。

        Args:
            rad_per_sec2: 加速度 [rad/s^2]

        """
        self._write(
            FeetechControlTable.PROFILE_ACCELERATION,
            rad_per_sec2_to_rev_per_min2(rad_per_sec2),
        )

    def get_profile_acceleration(self) -> float:
        """Profile Acceleration を取得する。

        Returns:
            加速度 [rad/s^2]

        """
        return rev_per_min2_to_rad_per_sec2(
            self._read(FeetechControlTable.PROFILE_ACCELERATION)
        )

    def set_profile_velocity(self, rad_per_sec: float) -> None:
        """Profile Velocity を設定する。

        Args:
            rad_per_sec: 速度 [rad/s]

        """
        self._write(
            FeetechControlTable.PROFILE_VELOCITY,
            rad_per_sec_to_rev_per_min(rad_per_sec),
        )

    def get_profile_velocity(self) -> float:
        """Profile Velocity を取得する。

        Returns:
            加速度 [rad/s^2]

        """
        return rev_per_min_to_rad_per_sec(
            self._read(FeetechControlTable.PROFILE_VELOCITY)
        )

    def set_goal_position(self, rad: float) -> None:
        """サーボの目標角度を設定する。

        Args:
            rad: 目標角度 [rad]

        """
        self._write(FeetechControlTable.GOAL_POSITION, rad_to_feetech_pulse(rad))

    def get_present_position(self) -> float:
        """サーボの現在角度を取得する。

        Returns:
            現在角度 [rad]

        """
        return feetech_pulse_to_rad(
            self._read(FeetechControlTable.PRESENT_POSITION)
        )

    def get_moving_state(self) -> bool:
        """サーボが動作中かどうか判定する。

        Returns:
            現在のサーボ状態

        """
        return not(self._read(FeetechControlTable.MOVING_STATUS))
