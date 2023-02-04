"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import abc
import akari_proto.m5stack_pb2
import google.protobuf.empty_pb2
import grpc
import typing

class M5StackServiceStub:
    def __init__(self, channel: grpc.Channel) -> None: ...
    SetPinOut: grpc.UnaryUnaryMultiCallable[
        akari_proto.m5stack_pb2.SetPinOutRequest,
        google.protobuf.empty_pb2.Empty]

    ResetPinOut: grpc.UnaryUnaryMultiCallable[
        akari_proto.m5stack_pb2.ResetPinOutRequest,
        google.protobuf.empty_pb2.Empty]

    SetDisplayColor: grpc.UnaryUnaryMultiCallable[
        akari_proto.m5stack_pb2.SetDisplayColorRequest,
        google.protobuf.empty_pb2.Empty]

    SetDisplayText: grpc.UnaryUnaryMultiCallable[
        akari_proto.m5stack_pb2.SetDisplayTextRequest,
        google.protobuf.empty_pb2.Empty]

    SetDisplayImage: grpc.UnaryUnaryMultiCallable[
        akari_proto.m5stack_pb2.SetDisplayImageRequest,
        google.protobuf.empty_pb2.Empty]

    Reset: grpc.UnaryUnaryMultiCallable[
        google.protobuf.empty_pb2.Empty,
        google.protobuf.empty_pb2.Empty]

    Get: grpc.UnaryUnaryMultiCallable[
        google.protobuf.empty_pb2.Empty,
        akari_proto.m5stack_pb2.M5StackStatus]

    GetStream: grpc.UnaryStreamMultiCallable[
        google.protobuf.empty_pb2.Empty,
        akari_proto.m5stack_pb2.M5StackStatus]


class M5StackServiceServicer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def SetPinOut(self,
        request: akari_proto.m5stack_pb2.SetPinOutRequest,
        context: grpc.ServicerContext,
    ) -> google.protobuf.empty_pb2.Empty: ...

    @abc.abstractmethod
    def ResetPinOut(self,
        request: akari_proto.m5stack_pb2.ResetPinOutRequest,
        context: grpc.ServicerContext,
    ) -> google.protobuf.empty_pb2.Empty: ...

    @abc.abstractmethod
    def SetDisplayColor(self,
        request: akari_proto.m5stack_pb2.SetDisplayColorRequest,
        context: grpc.ServicerContext,
    ) -> google.protobuf.empty_pb2.Empty: ...

    @abc.abstractmethod
    def SetDisplayText(self,
        request: akari_proto.m5stack_pb2.SetDisplayTextRequest,
        context: grpc.ServicerContext,
    ) -> google.protobuf.empty_pb2.Empty: ...

    @abc.abstractmethod
    def SetDisplayImage(self,
        request: akari_proto.m5stack_pb2.SetDisplayImageRequest,
        context: grpc.ServicerContext,
    ) -> google.protobuf.empty_pb2.Empty: ...

    @abc.abstractmethod
    def Reset(self,
        request: google.protobuf.empty_pb2.Empty,
        context: grpc.ServicerContext,
    ) -> google.protobuf.empty_pb2.Empty: ...

    @abc.abstractmethod
    def Get(self,
        request: google.protobuf.empty_pb2.Empty,
        context: grpc.ServicerContext,
    ) -> akari_proto.m5stack_pb2.M5StackStatus: ...

    @abc.abstractmethod
    def GetStream(self,
        request: google.protobuf.empty_pb2.Empty,
        context: grpc.ServicerContext,
    ) -> typing.Iterator[akari_proto.m5stack_pb2.M5StackStatus]: ...


def add_M5StackServiceServicer_to_server(servicer: M5StackServiceServicer, server: grpc.Server) -> None: ...
