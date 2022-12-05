import os
import pathlib
import tempfile
from typing import Iterator

import pytest
from akari_client.config import (
    JointManagerDynamixelSerialConfig,
    default_serial_config,
    load_env,
)


@pytest.fixture
def fake_os_env() -> Iterator[None]:
    old = os.environ.copy()
    try:
        yield
    finally:
        os.environ.clear()
        os.environ.update(old)


@pytest.fixture
def tempdir() -> Iterator[pathlib.Path]:
    with tempfile.TemporaryDirectory() as td:
        yield pathlib.Path(td)


def test_load_env(fake_os_env: None, tempdir: pathlib.Path) -> None:
    os.environ.clear()
    env = load_env()
    assert env.config_path is None

    config_path = tempdir / "foo.json"
    os.environ["AKARI_CLIENT_CONFIG_PATH"] = str(config_path)
    with pytest.raises(Exception):
        load_env()

    config_path.touch()
    env = load_env()
    assert env.config_path == config_path


def test_default_serial_config() -> None:
    config = default_serial_config()
    assert config.joint_manager is not None
    assert config.m5stack is not None
    assert isinstance(config.joint_manager, JointManagerDynamixelSerialConfig)
