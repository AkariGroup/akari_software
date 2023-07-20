from __future__ import annotations

import contextlib
import pathlib
import threading
from typing import Iterator

from scservo_sdk import *

DEFAULT_BAUDRATE = 115200
DEFAULT_DEVICE_NAME = pathlib.Path("/dev/serial0")
DEFAULT_PROTOCOL_END = 0

def get_baudrate_control_value(baudrate: int) -> int:
    """Feetechのボーレート設定値を取得する"""
    if baudrate == 115200:
        return 3
    elif baudrate == 57600:
        return 1
    else:
        raise ValueError("Either 57600 or 115200 is supported")


class FeetechCommunicator:
    def __init__(
        self,
        port_handler: PortHandler,
        packet_handler: PacketHandler,
    ) -> None:
        """feetechと通信を行うクラス

        Args:
            port_handler: feetech通信ポートのハンドラttyUSB_feetech
            packet_handler: feetechパケット通信のハンドラ
        """
        self._port_handler = port_handler
        self._packet_handler = packet_handler
        self._lock = threading.Lock()

    @classmethod
    @contextlib.contextmanager
    def open(
        cls,
        serial_port: pathlib.Path = DEFAULT_DEVICE_NAME,
        baudrate: int = DEFAULT_BAUDRATE,
    ) -> Iterator[FeetechCommunicator]:
        """feetechと通信を行うクラスを初期化する"""

        port_handler = PortHandler(str(serial_port))
        try:
            if port_handler.setBaudRate(baudrate):
                print("Succeeded to change the baudrate")
            else:
                raise RuntimeError("Failed to change the baudrate")

            if port_handler.openPort():
                print("Succeeded to open the port")
            else:
                raise RuntimeError("Failed to open port")

            packet_handler = PacketHandler(DEFAULT_PROTOCOL_END)
            yield cls(
                port_handler=port_handler,
                packet_handler=packet_handler,
            )
        finally:
            port_handler.closePort()

    def read(self, device_id: int, address: int, length: int) -> int:
        """feetechからデータを読み込む。

        Args:
            device_id: FeetechのID
            address: データアドレス
            length: データ長

        Returns:
            データ値

        """
        value: int
        result: int
        err: int

        with self._lock:
            if length == 1:
                value, result, err = self._packet_handler.read1ByteTxRx(
                    self._port_handler, device_id, address
                )
            elif length == 2:
                value, result, err = self._packet_handler.read2ByteTxRx(
                    self._port_handler, device_id, address
                )
            elif length == 4:
                value, result, err = self._packet_handler.read4ByteTxRx(
                    self._port_handler, device_id, address
                )
            else:
                raise ValueError(f"invalid length: {length}")

        if result != COMM_SUCCESS:
            raise RuntimeError(self._packet_handler.getTxRxResult(result))
        elif err != 0:
            raise RuntimeError(self._packet_handler.getRxPacketError(err))

        return value

    def write(self, device_id: int, address: int, length: int, value: int) -> None:
        """feetechにデータを書き込む。

        Args:
            device_id: FeetechのID
            address: データアドレス
            length: データ長
            value: データ値

        """
        result: int
        err: int

        with self._lock:
            if length == 1:
                result, err = self._packet_handler.write1ByteTxRx(
                    self._port_handler, device_id, address, value
                )
            elif length == 2:
                result, err = self._packet_handler.write2ByteTxRx(
                    self._port_handler, device_id, address, value
                )
            elif length == 4:
                result, err = self._packet_handler.write4ByteTxRx(
                    self._port_handler, device_id, address, value
                )
            else:
                raise ValueError(f"invalid length: {length}")

        if result != COMM_SUCCESS:
            raise RuntimeError(self._packet_handler.getTxRxResult(result))
        elif err != 0:
            raise RuntimeError(self._packet_handler.getRxPacketError(err))
