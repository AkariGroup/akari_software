from typing import cast

import pytest
from akari_client.serial.m5stack import M5StackSerialClient, _PinOut
from akari_client.serial.m5stack_communicator import M5SerialCommunicator

from ..mocks import MockM5Communicator


@pytest.fixture
def mock_communicator() -> M5SerialCommunicator:
    return cast(M5SerialCommunicator, MockM5Communicator())


def test__pin_out() -> None:
    pin_out = _PinOut()
    assert pin_out.serialize() == {"do0": 0, "do1": 0, "po0": 0}
    pin_out.dout0 = True
    pin_out.pwmout0 = 128
    assert pin_out.serialize() == {"do0": 1, "do1": 0, "po0": 128}

    pin_out.reset()
    assert pin_out.serialize() == {"do0": 0, "do1": 0, "po0": 0}


def test_set_dout(mock_communicator: M5SerialCommunicator) -> None:
    client = M5StackSerialClient(mock_communicator)

    client.set_dout(0, True)
    client.set_dout(1, True)

    with pytest.raises(ValueError):
        client.set_dout(2, True)


def test_set_pwmout(mock_communicator: M5SerialCommunicator) -> None:
    client = M5StackSerialClient(mock_communicator)

    client.set_pwmout(0, 255)

    with pytest.raises(ValueError):
        client.set_pwmout(1, 255)
