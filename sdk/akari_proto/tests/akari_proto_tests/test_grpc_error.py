from __future__ import annotations

from typing import Any, Dict

from akari_proto.grpc.error import RPCErrorSerializer


class CustomError(Exception):
    __name__ = "CustomError"

    def __init__(self, value: int) -> None:
        super().__init__()
        self.value = value

    def to_dict(self) -> Dict[str, Any]:
        return {"value": self.value}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> CustomError:
        return cls(data["value"])


def test_rpc_error_serializer() -> None:
    serializer = RPCErrorSerializer()
    ok_error = CustomError(10)
    ng_error = KeyError("hoge")

    assert serializer.serialize(ok_error) is None
    assert serializer.serialize(ng_error) is None
    assert serializer.deserialize("") is None
    assert serializer.deserialize("unknown") is None

    serializer.register(CustomError)
    payload = serializer.serialize(ok_error)
    assert payload is not None

    error = serializer.deserialize(payload)
    assert isinstance(error, CustomError)
    assert error.value == ok_error.value

    serializer2 = RPCErrorSerializer()
    assert serializer2.deserialize(payload) is None
