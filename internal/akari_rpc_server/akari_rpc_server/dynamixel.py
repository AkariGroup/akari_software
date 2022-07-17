from typing import Dict

import grpc
from akari_controller.dynamixel_controller import DynamixelController
from akari_proto import joints_controller_pb2, joints_controller_pb2_grpc
from google.protobuf.empty_pb2 import Empty


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

    def GetJointNames(
        self,
        request: Empty,
        context: grpc.ServicerContext,
    ) -> joints_controller_pb2.GetJointNamesResponse:
        return joints_controller_pb2.GetJointNamesResponse(
            joint_names=list(self._joints.keys()),
        )

    def GetServoEnabled(
        self,
        request: joints_controller_pb2.JointSpecifier,
        context: grpc.ServicerContext,
    ) -> joints_controller_pb2.GetServoEnabledResponse:
        joint = self._select_joint(request)
        return joints_controller_pb2.GetServoEnabledResponse(
            enabled=joint.get_servo_enabled(),
        )

    def SetServoEnabled(
        self,
        request: joints_controller_pb2.SetServoEnabledRequest,
        context: grpc.ServicerContext,
    ) -> Empty:
        joint = self._select_joint(request.target_joint)
        joint.set_servo_enabled(request.enabled)
        return Empty()

    def SetProfileAcceleration(
        self,
        request: joints_controller_pb2.SetProfileAccelerationRequest,
        context: grpc.ServicerContext,
    ) -> Empty:
        joint = self._select_joint(request.target_joint)
        joint.set_profile_acceleration(request.rad_per_sec2)
        return Empty()

    def SetProfileVelocity(
        self,
        request: joints_controller_pb2.SetProfileVelocityRequest,
        context: grpc.ServicerContext,
    ) -> Empty:
        joint = self._select_joint(request.target_joint)
        joint.set_profile_velocity(request.rad_per_sec)
        return Empty()

    def SetGoalPosition(
        self,
        request: joints_controller_pb2.SetGoalPositionRequest,
        context: grpc.ServicerContext,
    ) -> Empty:
        joint = self._select_joint(request.target_joint)
        joint.set_goal_position(request.rad)
        return Empty()

    def GetPresentPosition(
        self,
        request: joints_controller_pb2.JointSpecifier,
        context: grpc.ServicerContext,
    ) -> joints_controller_pb2.GetPresentPositionResponse:
        joint = self._select_joint(request)
        return joints_controller_pb2.GetPresentPositionResponse(
            rad=joint.get_present_position(),
        )
