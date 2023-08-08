from functools import lru_cache
from typing import List, Mapping, cast

import grpc
from akari_client.config import JointManagerDynamixelSerialConfig
from akari_client.joint_manager import JointManager
from akari_client.serial.dynamixel import DynamixelController
from akari_proto import joints_controller_pb2, joints_controller_pb2_grpc
from akari_proto.grpc.error import serialize_error
from google.protobuf.empty_pb2 import Empty

from . import dynamixel_init
from ._error import serializer


class DynamixelControllerServiceServicer(
    joints_controller_pb2_grpc.JointsControllerServiceServicer
):
    def __init__(
        self, config: JointManagerDynamixelSerialConfig, joint_manager: JointManager
    ) -> None:
        self._config = config
        self._joint_manager = joint_manager

    @lru_cache(1)
    def _initialize_joints(self) -> Mapping[str, DynamixelController]:
        # NOTE: When an exception is thrown in functions, `lru_cache` doesn't memoize the value
        # (i.e. the function is called again in that case)
        dynamixel_init.initialize_baudrate(self._config)

        jcs = self._joint_manager.joint_controllers
        assert all(isinstance(j, DynamixelController) for j in jcs)
        joint_controllers = cast(List[DynamixelController], jcs)

        dynamixel_init.initialize_joint_limit(
            joint_controllers,
            self._config,
        )
        dynamixel_init.initialize_default_velocity(
            joint_controllers,
            self._config,
        )
        dynamixel_init.initialize_default_acceleration(
            joint_controllers,
            self._config,
        )
        mapping = {j.joint_name: j for j in joint_controllers}
        _logger.error(f"Dynamixel initialize finished!")
        return mapping

    def _select_joint(
        self, specifier: joints_controller_pb2.JointSpecifier
    ) -> DynamixelController:
        joints = self._initialize_joints()
        joint = joints.get(specifier.joint_name)
        if joint is None:
            raise KeyError(f"Invalid joint name: {specifier.joint_name}")

        return joint

    @serialize_error(serializer)
    def GetPositionLimit(
        self,
        request: joints_controller_pb2.JointSpecifier,
        context: grpc.ServicerContext,
    ) -> joints_controller_pb2.GetPositionLimitResponse:
        joint = self._select_joint(request)
        return joints_controller_pb2.GetPositionLimitResponse(
            min=joint.get_position_limit().min,
            max=joint.get_position_limit().max,
        )

    @serialize_error(serializer)
    def GetJointNames(
        self,
        request: Empty,
        context: grpc.ServicerContext,
    ) -> joints_controller_pb2.GetJointNamesResponse:
        controllers = self._config.controllers
        return joints_controller_pb2.GetJointNamesResponse(
            joint_names=[c.joint_name for c in controllers],
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
    def GetProfileAcceleration(
        self,
        request: joints_controller_pb2.JointSpecifier,
        context: grpc.ServicerContext,
    ) -> joints_controller_pb2.GetProfileAccelerationResponse:
        joint = self._select_joint(request)
        return joints_controller_pb2.GetProfileAccelerationResponse(
            rad_per_sec2=joint.get_profile_acceleration(),
        )

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
    def GetProfileVelocity(
        self,
        request: joints_controller_pb2.JointSpecifier,
        context: grpc.ServicerContext,
    ) -> joints_controller_pb2.GetProfileVelocityResponse:
        joint = self._select_joint(request)
        return joints_controller_pb2.GetProfileVelocityResponse(
            rad_per_sec=joint.get_profile_velocity(),
        )

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

    @serialize_error(serializer)
    def GetMovingState(
        self,
        request: joints_controller_pb2.JointSpecifier,
        context: grpc.ServicerContext,
    ) -> joints_controller_pb2.GetMovingStateResponse:
        joint = self._select_joint(request)
        return joints_controller_pb2.GetMovingStateResponse(
            moving=joint.get_moving_state(),
        )
