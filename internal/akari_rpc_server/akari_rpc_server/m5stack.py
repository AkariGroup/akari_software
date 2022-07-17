import json
from typing import Iterator

import grpc
from akari_controller.color import Color
from akari_controller.m5serial_server_py import M5SerialServer
from akari_proto import m5stack_pb2, m5stack_pb2_grpc
from google.protobuf.empty_pb2 import Empty


def _as_akari_color(color: m5stack_pb2.Color) -> Color:
    return Color(
        color.red,
        color.green,
        color.blue,
    )


class M5StackServiceServicer(m5stack_pb2_grpc.M5StackServiceServicer):
    def __init__(self, m5stack: M5SerialServer) -> None:
        self._m5stack = m5stack

    def SetPinOut(
        self,
        request: m5stack_pb2.SetPinOutRequest,
        context: grpc.ServicerContext,
    ) -> Empty:
        pass

    def ResetPinOut(self, request: Empty, context: grpc.ServicerContext) -> Empty:
        self._m5stack.reset_allout(sync=True)
        return Empty()

    def SetDisplayColor(
        self, request: m5stack_pb2.SetDisplayColorRequest, context: grpc.ServicerContext
    ) -> Empty:
        self._m5stack.set_display_color(
            _as_akari_color(request.color),
            sync=request.sync,
        )
        return Empty()

    def SetDisplayText(
        self, request: m5stack_pb2.SetDisplayTextRequest, context: grpc.ServicerContext
    ) -> Empty:
        # TODO: Support Optional colors
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

    def UseJapaneseFont(
        self,
        request: m5stack_pb2.UseJapaneseFontRequest,
        context: grpc.ServicerContext,
    ) -> Empty:
        self._m5stack.use_japanese_font(
            request.enabled,
            sync=request.sync,
        )
        return Empty()

    def Reset(
        self,
        request: Empty,
        context: grpc.ServicerContext,
    ) -> Empty:
        self._m5stack.reset_m5()
        return Empty()

    def Get(
        self,
        request: Empty,
        context: grpc.ServicerContext,
    ) -> m5stack_pb2.M5StackStatus:
        data = self._m5stack.get()
        return m5stack_pb2.M5StackStatus(
            status_json=json.dumps(data),
        )

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
