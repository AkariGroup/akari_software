import contextlib
import logging
import pathlib
from typing import List, Literal, Optional, Union

import pydantic

from .joint_manager import JointManager
from .m5stack_client import M5StackClient

_logger = logging.getLogger(__name__)


class DynamixelControllerConfig(pydantic.BaseModel):
    joint_name: str
    dynamixel_id: int
    min_position_limit: float
    max_position_limit: float
    default_velocity: float
    default_acceleration: float


class JointManagerDynamixelSerialConfig(pydantic.BaseModel):
    type: Literal["dynamixel_serial"]
    controllers: List[DynamixelControllerConfig] = pydantic.Field(default=[])
    serial_port: pathlib.Path = pathlib.Path("/dev/ttyUSB_dynamixel")
    baudrate: int = 1000000
    protocol_version: float = 2.0

    def factory(self, stack: contextlib.ExitStack) -> JointManager:
        from .serial.factory import create_joint_manager

        _logger.debug("Initializing joint manager from 'dynamixel_serial' config")
        return create_joint_manager(self, stack)


class JointManagerGrpcConfig(pydantic.BaseModel):
    type: Literal["grpc"]
    endpoint: str
    joints: Optional[List[str]]

    def factory(self, stack: contextlib.ExitStack) -> JointManager:
        from .grpc.factory import create_joint_manager

        _logger.debug("Initializing joint manager from 'grpc' config")
        return create_joint_manager(self, stack)


JointManagerConfig = Union[JointManagerDynamixelSerialConfig, JointManagerGrpcConfig]


class M5StackSerialConfig(pydantic.BaseModel):
    type: Literal["serial"]
    serial_port: pathlib.Path = pathlib.Path("/dev/ttyUSB_M5Stack")
    baudrate: int = 500000
    serial_timeout: float = 0.2

    def factory(self, stack: contextlib.ExitStack) -> M5StackClient:
        from .serial.factory import create_m5stack_client

        _logger.debug("Initializing M5Stack client from 'serial' config")
        return create_m5stack_client(self, stack)


class M5StackGrpcConfig(pydantic.BaseModel):
    type: Literal["grpc"]
    endpoint: str

    def factory(self, stack: contextlib.ExitStack) -> M5StackClient:
        from .grpc.factory import create_m5stack_client

        _logger.debug("Initializing M5Stack client from 'grpc' config")
        return create_m5stack_client(self, stack)


M5StackConfig = Union[M5StackSerialConfig, M5StackGrpcConfig]


class AkariClientConfig(pydantic.BaseModel):
    joint_manager: JointManagerConfig = pydantic.Field(..., discriminator="type")
    m5stack: M5StackConfig = pydantic.Field(..., discriminator="type")


class AkariClientEnv(pydantic.BaseSettings):
    config_path: Optional[pydantic.FilePath] = None

    class Config:
        env_prefix = "AKARI_CLIENT_"
        case_sensitive = False


_CONFIG_LOOKUP_PATHS = [
    pathlib.Path("~/.config/akari/client_config.json"),
    pathlib.Path("/etc/akari/client_config.json"),
]


def load_env() -> AkariClientEnv:
    return AkariClientEnv()


def _load_config(path: pathlib.Path) -> AkariClientConfig:
    _logger.debug(f"Load config: {path}")
    return AkariClientConfig.parse_file(path)


def default_serial_config() -> AkariClientConfig:
    return AkariClientConfig(
        joint_manager=JointManagerDynamixelSerialConfig(type="dynamixel_serial"),
        m5stack=M5StackSerialConfig(type="serial"),
    )


def load_config() -> AkariClientConfig:
    env = load_env()
    if env.config_path is not None:
        _logger.debug("env.config_path is set")
        return _load_config(env.config_path)

    for path in _CONFIG_LOOKUP_PATHS:
        path = path.expanduser().resolve()
        if path.exists():
            return _load_config(path)

    _logger.debug("Use default config")
    return default_serial_config()
