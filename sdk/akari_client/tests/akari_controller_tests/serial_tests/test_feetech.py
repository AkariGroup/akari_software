import math
from typing import cast

import pytest
from akari_client.serial.feetech import (
    FeetechControlItem,
    FeetechController,
    FeetechControlTable,
    feetech_pulse_to_rad,
    rad_per_sec2_to_feetech_acc_pulse,
    rad_per_sec_to_feetech_vel_pulse,
    rad_to_feetech_pulse,
    feetech_acc_pulse_to_rad_per_sec2,
    feetech_vel_pulse_to_rad_per_sec,
)
from akari_client.serial.feetech_communicator import FeetechCommunicator

from ..mocks import MockFeetechCommunicator


@pytest.fixture
def mock_communicator() -> FeetechCommunicator:
    return cast(
        FeetechCommunicator, MockFeetechCommunicator(n_devices=2, n_address=256)
    )


def test_read_write_device(mock_communicator: FeetechCommunicator) -> None:
    controller1 = FeetechController("tilt", 0, mock_communicator)
    controller2 = FeetechController("pan", 1, mock_communicator)

    control = FeetechControlItem("foo", 100, 10)

    controller1._write(control, 0)
    controller2._write(control, 0)

    assert controller1._read(control) == 0
    assert controller2._read(control) == 0

    controller1._write(control, 10)
    assert controller1._read(control) == 10
    assert controller2._read(control) == 0

    controller2._write(control, 42)
    assert controller1._read(control) == 10
    assert controller2._read(control) == 42


def test_set_position_limit(mock_communicator: FeetechCommunicator) -> None:
    controller = FeetechController("tilt", 0, mock_communicator)
    assert controller.joint_name == "tilt"
    controller.set_position_limit(56, 78)
    assert controller._read(
        FeetechControlTable.MIN_POSITION_LIMIT
    ) == rad_to_feetech_pulse(56)
    assert controller._read(
        FeetechControlTable.MAX_POSITION_LIMIT
    ) == rad_to_feetech_pulse(78)


def test_get_position_limit(mock_communicator: FeetechCommunicator) -> None:
    controller = FeetechController("tilt", 0, mock_communicator)
    controller._write(FeetechControlTable.MIN_POSITION_LIMIT, rad_to_feetech_pulse(56))
    controller._write(FeetechControlTable.MAX_POSITION_LIMIT, rad_to_feetech_pulse(78))
    assert controller.get_position_limit().min == pytest.approx(56, rel=1e-2)
    assert controller.get_position_limit().max == pytest.approx(78, rel=1e-2)


def test_get_set_servo_enabled(
    mock_communicator: FeetechCommunicator,
) -> None:
    controller = FeetechController("tilt", 0, mock_communicator)

    controller.set_servo_enabled(False)
    assert not controller.get_servo_enabled()

    controller.set_servo_enabled(True)
    assert controller.get_servo_enabled()


def test_set_profile_acceleration(
    mock_communicator: FeetechCommunicator,
) -> None:
    controller = FeetechController("tilt", 0, mock_communicator)

    controller.set_profile_acceleration(123.4)
    assert controller._read(
        FeetechControlTable.PROFILE_ACCELERATION
    ) == rad_per_sec2_to_feetech_acc_pulse(123.4)


def test_get_profile_acceleration(
    mock_communicator: FeetechCommunicator,
) -> None:
    controller = FeetechController("tilt", 0, mock_communicator)

    controller._write(
        FeetechControlTable.PROFILE_ACCELERATION,
        rad_per_sec2_to_feetech_acc_pulse(123.4),
    )
    assert controller.get_profile_acceleration() == pytest.approx(123.4, rel=1e-2)


def test_set_profile_velocity(
    mock_communicator: FeetechCommunicator,
) -> None:
    controller = FeetechController("tilt", 0, mock_communicator)

    controller.set_profile_velocity(123.4)
    assert controller._read(
        FeetechControlTable.PROFILE_VELOCITY
    ) == rad_per_sec_tofeetech_vel_pulse(123.4)


def test_get_profile_velocity(
    mock_communicator: FeetechCommunicator,
) -> None:
    controller = FeetechController("tilt", 0, mock_communicator)

    controller._write(
        FeetechControlTable.PROFILE_VELOCITY, rad_per_sec_to_feetech_vel_pulse(123.4)
    )
    assert controller.get_profile_velocity() == pytest.approx(123.4, rel=1e-2)


def test_set_goal_position(
    mock_communicator: FeetechCommunicator,
) -> None:
    controller = FeetechController("tilt", 0, mock_communicator)

    controller.set_goal_position(123.4)
    assert controller._read(FeetechControlTable.GOAL_POSITION) == rad_to_feetech_pulse(
        123.4
    )


def test_get_present_position(
    mock_communicator: FeetechCommunicator,
) -> None:
    controller = FeetechController("tilt", 0, mock_communicator)

    controller._write(FeetechControlTable.PRESENT_POSITION, rad_to_feetech_pulse(123.4))
    assert controller.get_present_position() == pytest.approx(123.4, rel=1e-2)


def test_feetech_pulse_conversion() -> None:
    assert feetech_pulse_to_rad(rad_to_feetech_pulse(12.34)) == pytest.approx(
        12.34, rel=1e-2
    )
    assert rad_to_feetech_pulse(feetech_pulse_to_rad(4567)) == 4567


def test_rad_per_sec2_to_feetech_acc_pulse() -> None:
    expected = 12.34
    feetech_acc_pulse = rad_per_sec2_to_feetech_acc_pulse(expected)
    actual = feetech_acc_pulse * 8.789 * (math.pi / 180)
    assert expected == pytest.approx(actual, rel=1e-2)


def test_feetech_acc_pulse_to_rad_per_sec2() -> None:
    expected = 12
    rad_per_sec2 = feetech_acc_pulse_to_rad_per_sec2(expected)
    actual = rad_per_sec2 * (180 / math.pi) / 8.789
    assert expected == pytest.approx(actual, rel=1e-2)


def test_rad_per_sec_to_feetech_vel_pulse() -> None:
    expected = 12.34
    feetech_vel_pulse = rad_per_sec_to_feetech_vel_pulse(expected)
    actual = feetech_vel_pulse * 0.732 * (2 * math.pi) / 60
    assert expected == pytest.approx(actual, rel=1e-2)


def test_feetech_vel_pulse_to_rad_per_sec() -> None:
    expected = 12
    rad_per_sec = feetech_vel_pulse_to_rad_per_sec(expected)
    actual = rad_per_sec * 60 / (2 * math.pi) / 0.732
    assert expected == pytest.approx(actual, rel=1e-2)
