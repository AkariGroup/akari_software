from typing import List

import grpc
from akari_proto import joints_controller_pb2
from akari_proto.grpc.error import deserialize_error
from akari_proto.joints_controller_pb2_grpc import JointsControllerServiceStub
from google.protobuf.empty_pb2 import Empty

from ..joint_controller import PositionLimit, RevoluteJointController
from ._error import serializer


class _GrpcJointsController:
    def __init__(self, channel: grpc.Channel) -> None:
        self._stub = JointsControllerServiceStub(channel)

    @property
    def stub(self) -> JointsControllerServiceStub:
        return self._stub

    @deserialize_error(serializer)
    def get_joint_names(self) -> List[str]:
        res: joints_controller_pb2.GetJointNamesResponse = self._stub.GetJointNames(
            Empty()
        )
        return list(res.joint_names)


class GrpcJointController(RevoluteJointController):
    def __init__(self, joint_name: str, client: _GrpcJointsController) -> None:
        self._joint_name = joint_name
        self._client = client

    @deserialize_error(serializer)
    def get_position_limit(self) -> PositionLimit:
        res: joints_controller_pb2.GetPositionLimitResponse = (
            self._client.stub.GetPositionLimit(self.joint_specifier)
        )
        limit = PositionLimit(min=res.min, max=res.max)
        return limit

    @property
    def joint_name(self) -> str:
        return self._joint_name

    @property
    def joint_specifier(self) -> joints_controller_pb2.JointSpecifier:
        return joints_controller_pb2.JointSpecifier(
            joint_name=self._joint_name,
        )

    @deserialize_error(serializer)
    def get_servo_enabled(self) -> bool:
        res: joints_controller_pb2.GetServoEnabledResponse = (
            self._client.stub.GetServoEnabled(self.joint_specifier)
        )
        return res.enabled

    @deserialize_error(serializer)
    def set_servo_enabled(self, enabled: bool) -> None:
        request = joints_controller_pb2.SetServoEnabledRequest(
            target_joint=self.joint_specifier,
            enabled=enabled,
        )
        self._client.stub.SetServoEnabled(request)

    @deserialize_error(serializer)
    def set_profile_acceleration(self, rad_per_sec2: float) -> None:
        request = joints_controller_pb2.SetProfileAccelerationRequest(
            target_joint=self.joint_specifier,
            rad_per_sec2=rad_per_sec2,
        )
        self._client.stub.SetProfileAcceleration(request)

    @deserialize_error(serializer)
    def get_profile_acceleration(self) -> float:
        res: joints_controller_pb2.GetProfileAccelerationResponse = (
            self._client.stub.GetProfileAcceleration(self.joint_specifier)
        )
        return res.rad_per_sec2

    @deserialize_error(serializer)
    def set_profile_velocity(self, rad_per_sec: float) -> None:
        request = joints_controller_pb2.SetProfileVelocityRequest(
            target_joint=self.joint_specifier,
            rad_per_sec=rad_per_sec,
        )
        self._client.stub.SetProfileVelocity(request)

    @deserialize_error(serializer)
    def get_profile_velocity(self) -> float:
        res: joints_controller_pb2.GetProfileVelocityResponse = (
            self._client.stub.GetProfileVelocity(self.joint_specifier)
        )
        return res.rad_per_sec

    @deserialize_error(serializer)
    def set_goal_position(self, rad: float) -> None:
        request = joints_controller_pb2.SetGoalPositionRequest(
            target_joint=self.joint_specifier,
            rad=rad,
        )
        self._client.stub.SetGoalPosition(request)

    @deserialize_error(serializer)
    def get_present_position(self) -> float:
        res: joints_controller_pb2.GetPresentPositionResponse = (
            self._client.stub.GetPresentPosition(self.joint_specifier)
        )
        return res.rad

    @deserialize_error(serializer)
    def get_moving_state(self) -> bool:
        res: joints_controller_pb2.GetMovingStateResponse = (
            self._client.stub.GetMovingState(self.joint_specifier)
        )
        return res.moving
