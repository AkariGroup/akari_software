import contextlib
import signal
from concurrent.futures import ThreadPoolExecutor
from typing import Dict

import grpc
from akari_controller.akari_controller import DEFAULT_JOINT_CONFIGS
from akari_controller.dynamixel_communicator import DynamixelCommunicator
from akari_controller.dynamixel_controller import (
    DynamixelController,
    DynamixelControllerConfig,
)
from akari_controller.m5serial_server_py import M5SerialServer
from akari_proto import joints_controller_pb2_grpc, m5stack_pb2_grpc

from .dynamixel import DynamixelControllerServiceServicer
from .m5stack import M5StackServiceServicer


def initialize_dynamixel_controllers(
    communicator: DynamixelCommunicator,
) -> Dict[str, DynamixelController]:
    joints: Dict[str, DynamixelController] = {}

    for config in DEFAULT_JOINT_CONFIGS:
        # TODO: Dispatch ControllerInitialization by a config class
        assert isinstance(config, DynamixelControllerConfig)
        joints[config.joint_name] = DynamixelController(
            config,
            communicator,
        )

    return joints


def serve(port: int) -> None:
    with contextlib.ExitStack() as stack:
        dynamixel_communicator = stack.enter_context(DynamixelCommunicator.open())
        joints = initialize_dynamixel_controllers(dynamixel_communicator)
        m5stack = stack.enter_context(M5SerialServer())

        server = grpc.server(ThreadPoolExecutor(max_workers=10))
        joints_controller_pb2_grpc.add_JointsControllerServiceServicer_to_server(
            DynamixelControllerServiceServicer(joints),
            server,
        )
        m5stack_pb2_grpc.add_M5StackServiceServicer_to_server(
            M5StackServiceServicer(m5stack),
            server,
        )

        server.add_insecure_port("[::]:{}".format(port))
        server.start()

        print("grpc server has started")
        try:
            signal.pause()
        except KeyboardInterrupt:
            server.stop(0)
