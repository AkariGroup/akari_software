import math
from typing import cast

import pytest
from akari_client.dynamixel_communicator import DynamixelCommunicator
from akari_client.dynamixel_controller import (
    DynamixelControlItem,
    DynamixelController,
    DynamixelControllerConfig,
    DynamixelControlTable,
    dynamixel_pulse_to_rad,
    rad_per_sec2_to_rev_per_min2,
    rad_per_sec_to_rev_per_min,
    rad_to_dynamixel_pulse,
)

from .mocks import MockDynamixelCommunicator


@pytest.fixture
def mock_communicator() -> DynamixelCommunicator:
    return cast(
        DynamixelCommunicator, MockDynamixelCommunicator(n_devices=2, n_address=256)
    )


def test_read_write_device(mock_communicator: DynamixelCommunicator) -> None:
    controller1 = DynamixelController(
        DynamixelControllerConfig("tilt", 0, 0, 0), mock_communicator
    )
    controller2 = DynamixelController(
        DynamixelControllerConfig("pan", 1, 0, 0), mock_communicator
    )

    control = DynamixelControlItem("foo", 100, 10)

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


def test_set_position_limit(mock_communicator: DynamixelCommunicator) -> None:
    controller = DynamixelController(
        DynamixelControllerConfig("tilt", 0, 0, 0), mock_communicator
    )
    assert controller.joint_name == "tilt"
    controller.set_position_limit(56, 78)
    assert controller._read(
        DynamixelControlTable.MIN_POSITION_LIMIT
    ) == rad_to_dynamixel_pulse(56)
    assert controller._read(
        DynamixelControlTable.MAX_POSITION_LIMIT
    ) == rad_to_dynamixel_pulse(78)


def test_get_set_servo_enabled(
    mock_communicator: DynamixelCommunicator,
) -> None:
    controller = DynamixelController(
        DynamixelControllerConfig("tilt", 0, 0, 0), mock_communicator
    )

    controller.set_servo_enabled(False)
    assert not controller.get_servo_enabled()

    controller.set_servo_enabled(True)
    assert controller.get_servo_enabled()


def test_set_profile_acceleration(
    mock_communicator: DynamixelCommunicator,
) -> None:
    controller = DynamixelController(
        DynamixelControllerConfig("tilt", 0, 0, 0), mock_communicator
    )

    controller.set_profile_acceleration(123.4)
    assert controller._read(
        DynamixelControlTable.PROFILE_ACCELERATION
    ) == rad_per_sec2_to_rev_per_min2(123.4)


def test_set_profile_velocity(
    mock_communicator: DynamixelCommunicator,
) -> None:
    controller = DynamixelController(
        DynamixelControllerConfig("tilt", 0, 0, 0), mock_communicator
    )

    controller.set_profile_velocity(123.4)
    assert controller._read(
        DynamixelControlTable.PROFILE_VELOCITY
    ) == rad_per_sec_to_rev_per_min(123.4)


def test_set_goal_position(
    mock_communicator: DynamixelCommunicator,
) -> None:
    controller = DynamixelController(
        DynamixelControllerConfig("tilt", 0, 0, 0), mock_communicator
    )

    controller.set_goal_position(123.4)
    assert controller._read(
        DynamixelControlTable.GOAL_POSITION
    ) == rad_to_dynamixel_pulse(123.4)


def test_get_present_position(
    mock_communicator: DynamixelCommunicator,
) -> None:
    controller = DynamixelController(
        DynamixelControllerConfig("tilt", 0, 0, 0), mock_communicator
    )

    controller._write(
        DynamixelControlTable.PRESENT_POSITION, rad_to_dynamixel_pulse(123.4)
    )
    assert controller.get_present_position() == pytest.approx(123.4, rel=1e-2)


def test_dynamixel_pulse_conversion() -> None:
    assert dynamixel_pulse_to_rad(rad_to_dynamixel_pulse(12.34)) == pytest.approx(
        12.34, rel=1e-2
    )
    assert rad_to_dynamixel_pulse(dynamixel_pulse_to_rad(4567)) == 4567


def test_rad_per_sec2_to_rev_per_min2() -> None:
    expected = 12.34
    rev_per_min2 = rad_per_sec2_to_rev_per_min2(expected)
    actual = rev_per_min2 * 2.0 * math.pi / (60 * 60)
    assert expected == pytest.approx(actual, rel=1e-2)


def test_rad_per_sec_to_rev_per_min() -> None:
    expected = 12.34
    rev_per_min = rad_per_sec_to_rev_per_min(expected)
    actual = rev_per_min * 2.0 * math.pi / 60.0
    assert expected == pytest.approx(actual, rel=1e-2)
