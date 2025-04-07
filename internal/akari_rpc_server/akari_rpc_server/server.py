import contextlib
import logging
import signal
from concurrent.futures import ThreadPoolExecutor

import grpc
from akari_client.akari_client import AkariClient
from akari_client.config import (
    JointManagerDynamixelSerialConfig,
    JointManagerFeetechSerialConfig,
    M5StackSerialConfig,
    load_config,
)
from akari_client.serial.m5stack import M5StackSerialClient
from akari_proto import joints_controller_pb2_grpc, m5stack_pb2_grpc

from .dynamixel import DynamixelControllerServiceServicer
from .feetech import FeetechControllerServiceServicer
from .m5stack import M5StackServiceServicer


def serve(port: int) -> None:
    with contextlib.ExitStack() as stack:
        config = load_config()
        
        if not isinstance(config.joint_manager, JointManagerDynamixelSerialConfig) and not isinstance(config.joint_manager, JointManagerFeetechSerialConfig):
            logging.warning("Invalid JointManager configuration")
        if not isinstance(config.m5stack, M5StackSerialConfig):
            logging.warning("Invalid M5Stack configuration")

        client: AkariClient = stack.enter_context(AkariClient(config))
        joint_manager = None
        m5stack = None
        
        try:
            joint_manager = client.joints
        except RuntimeError as e:
            logging.warning(f"Servo motor initialization error: {e}")
            
        try:
            m5stack = client.m5stack
            if not isinstance(m5stack, M5StackSerialClient):
                logging.warning("M5Stack is of unexpected type")
                m5stack = None
        except RuntimeError as e:
            logging.warning(f"M5Stack initialization error: {e}")

        server = grpc.server(ThreadPoolExecutor(max_workers=10))
        
        if joint_manager is not None:
            if isinstance(config.joint_manager, JointManagerDynamixelSerialConfig):
                joints_controller_pb2_grpc.add_JointsControllerServiceServicer_to_server(
                    DynamixelControllerServiceServicer(config.joint_manager, joint_manager),
                    server,
                )
            elif isinstance(config.joint_manager, JointManagerFeetechSerialConfig):
                joints_controller_pb2_grpc.add_JointsControllerServiceServicer_to_server(
                    FeetechControllerServiceServicer(config.joint_manager, joint_manager),
                    server,
                )
        
        if m5stack is not None and isinstance(m5stack, M5StackSerialClient):
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
