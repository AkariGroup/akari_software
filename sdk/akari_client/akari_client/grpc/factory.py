import contextlib
import logging
from typing import List

from ..config import JointManagerGrpcConfig, M5StackGrpcConfig
from ..joint_manager import JointManager
from .channel_pool import create_channel
from .joints_controller import GrpcJointController, _GrpcJointsController
from .m5stack import GrpcM5StackClient

_logger = logging.getLogger(__name__)


def create_joint_manager(
    config: JointManagerGrpcConfig, stack: contextlib.ExitStack
) -> JointManager:
    channel = create_channel(stack, config.endpoint)
    service_client = _GrpcJointsController(channel)
    service_joints = service_client.get_joint_names()
    _logger.debug(f"Server response: service_joints='{service_joints}'")
    controllers: List[GrpcJointController] = []

    target_joints = config.joints or service_joints
    for joint_name in target_joints:
        if joint_name not in service_joints:
            raise ValueError(
                f"joint_name: '{joint_name}' is not supported in "
                f"gRPC server: '{config.endpoint}'"
            )

        _logger.debug(f"Use grpc controller for joint: '{joint_name}'")
        controllers.append(GrpcJointController(joint_name, service_client))

    return JointManager(controllers)


def create_m5stack_client(
    config: M5StackGrpcConfig, stack: contextlib.ExitStack
) -> GrpcM5StackClient:
    channel = create_channel(stack, config.endpoint)
    return GrpcM5StackClient(channel)
