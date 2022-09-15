# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from akari_proto import m5stack_pb2 as akari__proto_dot_m5stack__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


class M5StackServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SetPinOut = channel.unary_unary(
                '/akari_proto.M5StackService/SetPinOut',
                request_serializer=akari__proto_dot_m5stack__pb2.SetPinOutRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.ResetPinOut = channel.unary_unary(
                '/akari_proto.M5StackService/ResetPinOut',
                request_serializer=akari__proto_dot_m5stack__pb2.ResetPinOutRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.SetDisplayColor = channel.unary_unary(
                '/akari_proto.M5StackService/SetDisplayColor',
                request_serializer=akari__proto_dot_m5stack__pb2.SetDisplayColorRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.SetDisplayText = channel.unary_unary(
                '/akari_proto.M5StackService/SetDisplayText',
                request_serializer=akari__proto_dot_m5stack__pb2.SetDisplayTextRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.SetDisplayImage = channel.unary_unary(
                '/akari_proto.M5StackService/SetDisplayImage',
                request_serializer=akari__proto_dot_m5stack__pb2.SetDisplayImageRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.PlayMp3 = channel.unary_unary(
                '/akari_proto.M5StackService/PlayMp3',
                request_serializer=akari__proto_dot_m5stack__pb2.PlayMp3Request.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.StopMp3 = channel.unary_unary(
                '/akari_proto.M5StackService/StopMp3',
                request_serializer=akari__proto_dot_m5stack__pb2.StopMp3Request.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.Reset = channel.unary_unary(
                '/akari_proto.M5StackService/Reset',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.Get = channel.unary_unary(
                '/akari_proto.M5StackService/Get',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=akari__proto_dot_m5stack__pb2.M5StackStatus.FromString,
                )
        self.GetStream = channel.unary_stream(
                '/akari_proto.M5StackService/GetStream',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=akari__proto_dot_m5stack__pb2.M5StackStatus.FromString,
                )


class M5StackServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def SetPinOut(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ResetPinOut(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SetDisplayColor(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SetDisplayText(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SetDisplayImage(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def PlayMp3(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def StopMp3(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Reset(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Get(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetStream(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_M5StackServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SetPinOut': grpc.unary_unary_rpc_method_handler(
                    servicer.SetPinOut,
                    request_deserializer=akari__proto_dot_m5stack__pb2.SetPinOutRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'ResetPinOut': grpc.unary_unary_rpc_method_handler(
                    servicer.ResetPinOut,
                    request_deserializer=akari__proto_dot_m5stack__pb2.ResetPinOutRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'SetDisplayColor': grpc.unary_unary_rpc_method_handler(
                    servicer.SetDisplayColor,
                    request_deserializer=akari__proto_dot_m5stack__pb2.SetDisplayColorRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'SetDisplayText': grpc.unary_unary_rpc_method_handler(
                    servicer.SetDisplayText,
                    request_deserializer=akari__proto_dot_m5stack__pb2.SetDisplayTextRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'SetDisplayImage': grpc.unary_unary_rpc_method_handler(
                    servicer.SetDisplayImage,
                    request_deserializer=akari__proto_dot_m5stack__pb2.SetDisplayImageRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'PlayMp3': grpc.unary_unary_rpc_method_handler(
                    servicer.PlayMp3,
                    request_deserializer=akari__proto_dot_m5stack__pb2.PlayMp3Request.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'StopMp3': grpc.unary_unary_rpc_method_handler(
                    servicer.StopMp3,
                    request_deserializer=akari__proto_dot_m5stack__pb2.StopMp3Request.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'Reset': grpc.unary_unary_rpc_method_handler(
                    servicer.Reset,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'Get': grpc.unary_unary_rpc_method_handler(
                    servicer.Get,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=akari__proto_dot_m5stack__pb2.M5StackStatus.SerializeToString,
            ),
            'GetStream': grpc.unary_stream_rpc_method_handler(
                    servicer.GetStream,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=akari__proto_dot_m5stack__pb2.M5StackStatus.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'akari_proto.M5StackService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class M5StackService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def SetPinOut(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/akari_proto.M5StackService/SetPinOut',
            akari__proto_dot_m5stack__pb2.SetPinOutRequest.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ResetPinOut(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/akari_proto.M5StackService/ResetPinOut',
            akari__proto_dot_m5stack__pb2.ResetPinOutRequest.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SetDisplayColor(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/akari_proto.M5StackService/SetDisplayColor',
            akari__proto_dot_m5stack__pb2.SetDisplayColorRequest.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SetDisplayText(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/akari_proto.M5StackService/SetDisplayText',
            akari__proto_dot_m5stack__pb2.SetDisplayTextRequest.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SetDisplayImage(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/akari_proto.M5StackService/SetDisplayImage',
            akari__proto_dot_m5stack__pb2.SetDisplayImageRequest.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def PlayMp3(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/akari_proto.M5StackService/PlayMp3',
            akari__proto_dot_m5stack__pb2.PlayMp3Request.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def StopMp3(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/akari_proto.M5StackService/StopMp3',
            akari__proto_dot_m5stack__pb2.StopMp3Request.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Reset(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/akari_proto.M5StackService/Reset',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Get(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/akari_proto.M5StackService/Get',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            akari__proto_dot_m5stack__pb2.M5StackStatus.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetStream(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/akari_proto.M5StackService/GetStream',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            akari__proto_dot_m5stack__pb2.M5StackStatus.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
