import json
from typing import Dict, Iterator, cast

import grpc
from akari_client.color import Color, Colors
from akari_client.position import Positions
from akari_proto import m5stack_pb2
from akari_proto.grpc.error import deserialize_error
from akari_proto.m5stack_pb2_grpc import M5StackServiceStub
from google.protobuf.empty_pb2 import Empty

from ..m5stack_client import M5ComDict, M5StackClient
from ._error import serializer


def _as_proto_color(color: Color) -> m5stack_pb2.Color:
    return m5stack_pb2.Color(
        red=color.red,
        green=color.green,
        blue=color.blue,
    )


class GrpcM5StackClient(M5StackClient):
    def __init__(self, channel: grpc.Channel) -> None:
        self._stub = M5StackServiceStub(channel)

    @deserialize_error(serializer)
    def set_dout(self, pin_id: int, value: bool, sync: bool = True) -> None:
        binary_pins: Dict[str, bool] = {}
        if pin_id == 0:
            binary_pins["dout0"] = value
        elif pin_id == 1:
            binary_pins["dout1"] = value
        else:
            raise ValueError(f"Out of range pin_id: {pin_id}")

        request = m5stack_pb2.SetPinOutRequest(
            binary_pins=binary_pins,
            sync=sync,
        )
        self._stub.SetPinOut(request)

    @deserialize_error(serializer)
    def set_pwmout(self, pin_id: int, value: int, sync: bool = True) -> None:
        int_pins: Dict[str, int] = {}
        if pin_id == 0:
            int_pins["pwmout0"] = value
        else:
            raise ValueError(f"Out of range pin_id: {pin_id}")

        request = m5stack_pb2.SetPinOutRequest(
            int_pins=int_pins,
            sync=sync,
        )
        self._stub.SetPinOut(request)

    @deserialize_error(serializer)
    def set_allout(
        self,
        *,
        dout0: bool,
        dout1: bool,
        pwmout0: int,
        sync: bool = True,
    ) -> None:
        binary_pins: Dict[str, bool] = {
            "dout0": dout0,
            "dout1": dout1,
        }
        int_pins: Dict[str, int] = {
            "pwmout0": pwmout0,
        }
        request = m5stack_pb2.SetPinOutRequest(
            binary_pins=binary_pins,
            int_pins=int_pins,
            sync=sync,
        )
        self._stub.SetPinOut(request)

    @deserialize_error(serializer)
    def reset_allout(self, sync: bool = True) -> None:
        self._stub.ResetPinOut(m5stack_pb2.ResetPinOutRequest(sync=sync))

    @deserialize_error(serializer)
    def set_display_color(self, color: Color, sync: bool = True) -> None:
        request = m5stack_pb2.SetDisplayColorRequest(
            color=_as_proto_color(color),
            sync=sync,
        )
        self._stub.SetDisplayColor(request)

    @deserialize_error(serializer)
    def set_display_text(
        self,
        text: str,
        pos_x: int = Positions.CENTER,
        pos_y: int = Positions.CENTER,
        size: int = 3,
        text_color: Color = Colors.BLACK,
        back_color: Color = Colors.WHITE,
        refresh: bool = True,
        sync: bool = True,
    ) -> None:
        request = m5stack_pb2.SetDisplayTextRequest(
            text=text,
            pos_x=pos_x,
            pos_y=pos_y,
            size=size,
            text_color=_as_proto_color(text_color),
            bg_color=_as_proto_color(back_color),
            refresh=refresh,
            sync=sync,
        )
        self._stub.SetDisplayText(request)

    @deserialize_error(serializer)
    def set_display_image(
        self,
        filepath: str,
        pos_x: int = Positions.CENTER,
        pos_y: int = Positions.CENTER,
        scale: float = -1.0,
        sync: bool = True,
    ) -> None:
        request = m5stack_pb2.SetDisplayImageRequest(
            path=filepath,
            pos_x=pos_x,
            pos_y=pos_y,
            scale=scale,
            sync=sync,
        )
        self._stub.SetDisplayImage(request)

    @deserialize_error(serializer)
    def play_mp3(self, filepath: str, sync: bool = True) -> None:
        request = m5stack_pb2.PlayMp3Request(
            path=filepath,
            sync=sync,
        )
        self._stub.PlayMp3(request)

    @deserialize_error(serializer)
    def stop_mp3(self, sync: bool = True) -> None:
        request = m5stack_pb2.StopMp3Request(
            sync=sync,
        )
        self._stub.StopMp3(request)

    @deserialize_error(serializer)
    def reset_m5(self) -> None:
        self._stub.Reset(Empty())

    @deserialize_error(serializer)
    def get(self) -> M5ComDict:
        data: m5stack_pb2.M5StackStatus = self._stub.Get(Empty())
        return cast(M5ComDict, json.loads(data.status_json))

    @deserialize_error(serializer)
    def get_stream(self) -> Iterator[M5ComDict]:
        stream = self._stub.GetStream(Empty())
        for r in stream:
            data: m5stack_pb2.M5StackStatus = r
            yield cast(M5ComDict, json.loads(data.status_json))
