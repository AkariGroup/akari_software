from typing import cast

import pytest
from akari_controller.m5serial_communicator import M5SerialCommunicator
from akari_controller.m5serial_server_py import M5SerialServer

from .mocks import MockM5Communicator


@pytest.fixture
def mock_communicator() -> M5SerialCommunicator:
    return cast(M5SerialCommunicator, MockM5Communicator())


def test_set_dout(mock_communicator: M5SerialCommunicator) -> None:
    client = M5SerialServer(mock_communicator)

    client.set_dout(0, True)
    client.set_dout(1, True)

    with pytest.raises(ValueError):
        client.set_dout(2, True)


def test_set_pwmout(mock_communicator: M5SerialCommunicator) -> None:
    client = M5SerialServer(mock_communicator)

    client.set_pwmout(0, 255)

    with pytest.raises(ValueError):
        client.set_pwmout(1, 255)
