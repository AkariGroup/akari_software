import contextlib
import signal
from concurrent.futures import ThreadPoolExecutor

import grpc
from akari_client.serial.dynamixel import create_controllers
from akari_client.serial.dynamixel_communicator import DynamixelCommunicator
from akari_client.serial.m5stack import M5StackSerialClient
from akari_proto import joints_controller_pb2_grpc, m5stack_pb2_grpc

from .dynamixel import DynamixelControllerServiceServicer
from .m5stack import M5StackServiceServicer


def serve(port: int) -> None:
    with contextlib.ExitStack() as stack:
        dynamixel_communicator = stack.enter_context(DynamixelCommunicator.open())
        joints = create_controllers(dynamixel_communicator)
        m5stack = stack.enter_context(M5StackSerialClient())

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
