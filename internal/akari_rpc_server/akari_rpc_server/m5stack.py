import json
from typing import Any, Dict, Iterator, Optional

import grpc
from akari_client.color import Color
from akari_client.serial.m5stack import M5StackSerialClient
from akari_proto import m5stack_pb2, m5stack_pb2_grpc
from akari_proto.grpc.error import serialize_error
from google.protobuf.empty_pb2 import Empty

from ._error import serializer


def _as_akari_color(color: m5stack_pb2.Color) -> Optional[Color]:
    if color.red == -1 and color.green == -1 and color.blue == -1:
        return None

    return Color(
        color.red,
        color.green,
        color.blue,
    )


def _validate_pinout_request(request: m5stack_pb2.SetPinOutRequest) -> None:
    supported_bools = ["dout0", "dout1"]
    supported_ints = ["pwmout0"]

    for k in request.binary_pins.keys():
        if k not in supported_bools:
            raise KeyError(f"Unsupported binary pin: {k}")

    for k in request.int_pins.keys():
        if k not in supported_ints:
            raise KeyError(f"Unsupported int pin: {k}")


class M5StackServiceServicer(m5stack_pb2_grpc.M5StackServiceServicer):
    def __init__(self, m5stack: M5StackSerialClient) -> None:
        self._m5stack = m5stack

    @serialize_error(serializer)
    def SetPinOut(
        self,
        request: m5stack_pb2.SetPinOutRequest,
        context: grpc.ServicerContext,
    ) -> Empty:
        _validate_pinout_request(request)
        args: Dict[str, Any] = {}
        args.update(request.binary_pins.items())
        args.update(request.int_pins.items())

        self._m5stack.set_allout(
            sync=request.sync,
            **args,
        )
        return Empty()

    @serialize_error(serializer)
    def ResetPinOut(
        self, request: m5stack_pb2.ResetPinOutRequest, context: grpc.ServicerContext
    ) -> Empty:
        self._m5stack.reset_allout(sync=request.sync)
        return Empty()

    @serialize_error(serializer)
    def SetDisplayColor(
        self, request: m5stack_pb2.SetDisplayColorRequest, context: grpc.ServicerContext
    ) -> Empty:
        color = _as_akari_color(request.color)
        if color is not None:
            self._m5stack.set_display_color(
                color=color,
                sync=request.sync,
            )
        return Empty()

    @serialize_error(serializer)
    def SetDisplayText(
        self, request: m5stack_pb2.SetDisplayTextRequest, context: grpc.ServicerContext
    ) -> Empty:
        self._m5stack.set_display_text(
            text=request.text,
            pos_x=request.pos_x,
            pos_y=request.pos_y,
            size=request.size,
            text_color=_as_akari_color(request.text_color),
            back_color=_as_akari_color(request.bg_color),
            refresh=request.refresh,
            sync=request.sync,
        )
        return Empty()

    @serialize_error(serializer)
    def SetDisplayImage(
        self,
        request: m5stack_pb2.SetDisplayImageRequest,
        context: grpc.ServicerContext,
    ) -> Empty:
        self._m5stack.set_display_image(
            request.path,
            pos_x=request.pos_x,
            pos_y=request.pos_y,
            scale=request.scale,
            sync=request.sync,
        )
        return Empty()

    @serialize_error(serializer)
    def Reset(
        self,
        request: Empty,
        context: grpc.ServicerContext,
    ) -> Empty:
        self._m5stack.reset_m5()
        return Empty()

    @serialize_error(serializer)
    def Get(
        self,
        request: Empty,
        context: grpc.ServicerContext,
    ) -> m5stack_pb2.M5StackStatus:
        data = self._m5stack.get()
        return m5stack_pb2.M5StackStatus(
            status_json=json.dumps(data),
        )

    @serialize_error(serializer)
    def GetStream(
        self,
        request: Empty,
        context: grpc.ServicerContext,
    ) -> Iterator[m5stack_pb2.M5StackStatus]:
        while True:
            data = self._m5stack.get()
            yield m5stack_pb2.M5StackStatus(
                status_json=json.dumps(data),
            )
