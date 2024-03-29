# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from akari_proto import joints_controller_pb2 as akari__proto_dot_joints__controller__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


class JointsControllerServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetPositionLimit = channel.unary_unary(
                '/akari_proto.JointsControllerService/GetPositionLimit',
                request_serializer=akari__proto_dot_joints__controller__pb2.JointSpecifier.SerializeToString,
                response_deserializer=akari__proto_dot_joints__controller__pb2.GetPositionLimitResponse.FromString,
                )
        self.GetJointNames = channel.unary_unary(
                '/akari_proto.JointsControllerService/GetJointNames',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=akari__proto_dot_joints__controller__pb2.GetJointNamesResponse.FromString,
                )
        self.GetServoEnabled = channel.unary_unary(
                '/akari_proto.JointsControllerService/GetServoEnabled',
                request_serializer=akari__proto_dot_joints__controller__pb2.JointSpecifier.SerializeToString,
                response_deserializer=akari__proto_dot_joints__controller__pb2.GetServoEnabledResponse.FromString,
                )
        self.SetServoEnabled = channel.unary_unary(
                '/akari_proto.JointsControllerService/SetServoEnabled',
                request_serializer=akari__proto_dot_joints__controller__pb2.SetServoEnabledRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.SetProfileAcceleration = channel.unary_unary(
                '/akari_proto.JointsControllerService/SetProfileAcceleration',
                request_serializer=akari__proto_dot_joints__controller__pb2.SetProfileAccelerationRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.GetProfileAcceleration = channel.unary_unary(
                '/akari_proto.JointsControllerService/GetProfileAcceleration',
                request_serializer=akari__proto_dot_joints__controller__pb2.JointSpecifier.SerializeToString,
                response_deserializer=akari__proto_dot_joints__controller__pb2.GetProfileAccelerationResponse.FromString,
                )
        self.SetProfileVelocity = channel.unary_unary(
                '/akari_proto.JointsControllerService/SetProfileVelocity',
                request_serializer=akari__proto_dot_joints__controller__pb2.SetProfileVelocityRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.GetProfileVelocity = channel.unary_unary(
                '/akari_proto.JointsControllerService/GetProfileVelocity',
                request_serializer=akari__proto_dot_joints__controller__pb2.JointSpecifier.SerializeToString,
                response_deserializer=akari__proto_dot_joints__controller__pb2.GetProfileVelocityResponse.FromString,
                )
        self.SetGoalPosition = channel.unary_unary(
                '/akari_proto.JointsControllerService/SetGoalPosition',
                request_serializer=akari__proto_dot_joints__controller__pb2.SetGoalPositionRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.GetPresentPosition = channel.unary_unary(
                '/akari_proto.JointsControllerService/GetPresentPosition',
                request_serializer=akari__proto_dot_joints__controller__pb2.JointSpecifier.SerializeToString,
                response_deserializer=akari__proto_dot_joints__controller__pb2.GetPresentPositionResponse.FromString,
                )
        self.GetMovingState = channel.unary_unary(
                '/akari_proto.JointsControllerService/GetMovingState',
                request_serializer=akari__proto_dot_joints__controller__pb2.JointSpecifier.SerializeToString,
                response_deserializer=akari__proto_dot_joints__controller__pb2.GetMovingStateResponse.FromString,
                )


class JointsControllerServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetPositionLimit(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetJointNames(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetServoEnabled(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SetServoEnabled(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SetProfileAcceleration(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetProfileAcceleration(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SetProfileVelocity(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetProfileVelocity(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SetGoalPosition(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetPresentPosition(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetMovingState(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_JointsControllerServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetPositionLimit': grpc.unary_unary_rpc_method_handler(
                    servicer.GetPositionLimit,
                    request_deserializer=akari__proto_dot_joints__controller__pb2.JointSpecifier.FromString,
                    response_serializer=akari__proto_dot_joints__controller__pb2.GetPositionLimitResponse.SerializeToString,
            ),
            'GetJointNames': grpc.unary_unary_rpc_method_handler(
                    servicer.GetJointNames,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=akari__proto_dot_joints__controller__pb2.GetJointNamesResponse.SerializeToString,
            ),
            'GetServoEnabled': grpc.unary_unary_rpc_method_handler(
                    servicer.GetServoEnabled,
                    request_deserializer=akari__proto_dot_joints__controller__pb2.JointSpecifier.FromString,
                    response_serializer=akari__proto_dot_joints__controller__pb2.GetServoEnabledResponse.SerializeToString,
            ),
            'SetServoEnabled': grpc.unary_unary_rpc_method_handler(
                    servicer.SetServoEnabled,
                    request_deserializer=akari__proto_dot_joints__controller__pb2.SetServoEnabledRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'SetProfileAcceleration': grpc.unary_unary_rpc_method_handler(
                    servicer.SetProfileAcceleration,
                    request_deserializer=akari__proto_dot_joints__controller__pb2.SetProfileAccelerationRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'GetProfileAcceleration': grpc.unary_unary_rpc_method_handler(
                    servicer.GetProfileAcceleration,
                    request_deserializer=akari__proto_dot_joints__controller__pb2.JointSpecifier.FromString,
                    response_serializer=akari__proto_dot_joints__controller__pb2.GetProfileAccelerationResponse.SerializeToString,
            ),
            'SetProfileVelocity': grpc.unary_unary_rpc_method_handler(
                    servicer.SetProfileVelocity,
                    request_deserializer=akari__proto_dot_joints__controller__pb2.SetProfileVelocityRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'GetProfileVelocity': grpc.unary_unary_rpc_method_handler(
                    servicer.GetProfileVelocity,
                    request_deserializer=akari__proto_dot_joints__controller__pb2.JointSpecifier.FromString,
                    response_serializer=akari__proto_dot_joints__controller__pb2.GetProfileVelocityResponse.SerializeToString,
            ),
            'SetGoalPosition': grpc.unary_unary_rpc_method_handler(
                    servicer.SetGoalPosition,
                    request_deserializer=akari__proto_dot_joints__controller__pb2.SetGoalPositionRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'GetPresentPosition': grpc.unary_unary_rpc_method_handler(
                    servicer.GetPresentPosition,
                    request_deserializer=akari__proto_dot_joints__controller__pb2.JointSpecifier.FromString,
                    response_serializer=akari__proto_dot_joints__controller__pb2.GetPresentPositionResponse.SerializeToString,
            ),
            'GetMovingState': grpc.unary_unary_rpc_method_handler(
                    servicer.GetMovingState,
                    request_deserializer=akari__proto_dot_joints__controller__pb2.JointSpecifier.FromString,
                    response_serializer=akari__proto_dot_joints__controller__pb2.GetMovingStateResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'akari_proto.JointsControllerService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class JointsControllerService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetPositionLimit(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/akari_proto.JointsControllerService/GetPositionLimit',
            akari__proto_dot_joints__controller__pb2.JointSpecifier.SerializeToString,
            akari__proto_dot_joints__controller__pb2.GetPositionLimitResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetJointNames(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/akari_proto.JointsControllerService/GetJointNames',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            akari__proto_dot_joints__controller__pb2.GetJointNamesResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetServoEnabled(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/akari_proto.JointsControllerService/GetServoEnabled',
            akari__proto_dot_joints__controller__pb2.JointSpecifier.SerializeToString,
            akari__proto_dot_joints__controller__pb2.GetServoEnabledResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SetServoEnabled(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/akari_proto.JointsControllerService/SetServoEnabled',
            akari__proto_dot_joints__controller__pb2.SetServoEnabledRequest.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SetProfileAcceleration(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/akari_proto.JointsControllerService/SetProfileAcceleration',
            akari__proto_dot_joints__controller__pb2.SetProfileAccelerationRequest.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetProfileAcceleration(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/akari_proto.JointsControllerService/GetProfileAcceleration',
            akari__proto_dot_joints__controller__pb2.JointSpecifier.SerializeToString,
            akari__proto_dot_joints__controller__pb2.GetProfileAccelerationResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SetProfileVelocity(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/akari_proto.JointsControllerService/SetProfileVelocity',
            akari__proto_dot_joints__controller__pb2.SetProfileVelocityRequest.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetProfileVelocity(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/akari_proto.JointsControllerService/GetProfileVelocity',
            akari__proto_dot_joints__controller__pb2.JointSpecifier.SerializeToString,
            akari__proto_dot_joints__controller__pb2.GetProfileVelocityResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SetGoalPosition(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/akari_proto.JointsControllerService/SetGoalPosition',
            akari__proto_dot_joints__controller__pb2.SetGoalPositionRequest.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetPresentPosition(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/akari_proto.JointsControllerService/GetPresentPosition',
            akari__proto_dot_joints__controller__pb2.JointSpecifier.SerializeToString,
            akari__proto_dot_joints__controller__pb2.GetPresentPositionResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetMovingState(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/akari_proto.JointsControllerService/GetMovingState',
            akari__proto_dot_joints__controller__pb2.JointSpecifier.SerializeToString,
            akari__proto_dot_joints__controller__pb2.GetMovingStateResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
