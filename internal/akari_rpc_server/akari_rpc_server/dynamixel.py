from typing import Dict

import grpc
from akari_client.serial.dynamixel import DynamixelController
from akari_proto import joints_controller_pb2, joints_controller_pb2_grpc
from akari_proto.grpc.error import serialize_error
from google.protobuf.empty_pb2 import Empty

from ._error import serializer


class DynamixelControllerServiceServicer(
    joints_controller_pb2_grpc.JointsControllerServiceServicer
):
    def __init__(self, joints: Dict[str, DynamixelController]) -> None:
        self._joints = joints

    def _select_joint(
        self, specifier: joints_controller_pb2.JointSpecifier
    ) -> DynamixelController:
        joint = self._joints.get(specifier.joint_name)
        if joint is None:
            raise KeyError(f"Invalid joint name: {specifier.joint_name}")

        return joint

    @serialize_error(serializer)
    def GetJointNames(
        self,
        request: Empty,
        context: grpc.ServicerContext,
    ) -> joints_controller_pb2.GetJointNamesResponse:
        return joints_controller_pb2.GetJointNamesResponse(
            joint_names=list(self._joints.keys()),
        )

    @serialize_error(serializer)
    def GetServoEnabled(
        self,
        request: joints_controller_pb2.JointSpecifier,
        context: grpc.ServicerContext,
    ) -> joints_controller_pb2.GetServoEnabledResponse:
        joint = self._select_joint(request)
        return joints_controller_pb2.GetServoEnabledResponse(
            enabled=joint.get_servo_enabled(),
        )

    @serialize_error(serializer)
    def SetServoEnabled(
        self,
        request: joints_controller_pb2.SetServoEnabledRequest,
        context: grpc.ServicerContext,
    ) -> Empty:
        joint = self._select_joint(request.target_joint)
        joint.set_servo_enabled(request.enabled)
        return Empty()

    @serialize_error(serializer)
    def SetProfileAcceleration(
        self,
        request: joints_controller_pb2.SetProfileAccelerationRequest,
        context: grpc.ServicerContext,
    ) -> Empty:
        joint = self._select_joint(request.target_joint)
        joint.set_profile_acceleration(request.rad_per_sec2)
        return Empty()

    @serialize_error(serializer)
    def SetProfileVelocity(
        self,
        request: joints_controller_pb2.SetProfileVelocityRequest,
        context: grpc.ServicerContext,
    ) -> Empty:
        joint = self._select_joint(request.target_joint)
        joint.set_profile_velocity(request.rad_per_sec)
        return Empty()

    @serialize_error(serializer)
    def SetGoalPosition(
        self,
        request: joints_controller_pb2.SetGoalPositionRequest,
        context: grpc.ServicerContext,
    ) -> Empty:
        joint = self._select_joint(request.target_joint)
        joint.set_goal_position(request.rad)
        return Empty()

    @serialize_error(serializer)
    def GetPresentPosition(
        self,
        request: joints_controller_pb2.JointSpecifier,
        context: grpc.ServicerContext,
    ) -> joints_controller_pb2.GetPresentPositionResponse:
        joint = self._select_joint(request)
        return joints_controller_pb2.GetPresentPositionResponse(
            rad=joint.get_present_position(),
        )
