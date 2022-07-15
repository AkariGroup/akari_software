from __future__ import annotations

import json
import threading
import time
from typing import Any, Dict, Optional, TypedDict, cast

import serial

BAUDRATE = 500000
DEVICE_NAME = "/dev/ttyUSB_M5Stack"
TIMEOUT = 0.2


class M5ComDict(TypedDict):
    din0: bool
    din1: bool
    ain0: int
    dout0: bool
    dout1: bool
    pwmout0: int
    general0: float
    general1: float
    button_a: bool
    button_b: bool
    button_c: bool
    temperature: float
    pressure: float
    brightness: int
    time: float
    is_response: bool


class M5SerialCommunicator:
    def __init__(self) -> None:
        self._reference_time = time.time()

        self._condition = threading.Condition()
        self._latest_msg: Optional[M5ComDict] = None
        self._thread: Optional[threading.Thread] = None
        self._exit = False

        self._serial = serial.Serial(
            baudrate=BAUDRATE, port=DEVICE_NAME, timeout=TIMEOUT
        )

    def __enter__(self) -> M5SerialCommunicator:
        return self

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        self.stop()

    def start(self) -> None:
        if self._thread is not None:
            return

        self._exit = False
        self._thread = threading.Thread(target=self._read, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        thread = self._thread
        if thread is None:
            return
        self._thread = None

        self._exit = True
        if thread.is_alive():
            thread.join()

    def _read_line(self) -> None:
        res: Dict[str, Any] = {}
        data_str = self._serial.readline().decode("utf-8")
        received = json.loads(data_str)
        res["din0"] = bool(received["io"]["di0"])
        res["din1"] = bool(received["io"]["di1"])
        res["ain0"] = int(received["io"]["ai0"])
        res["dout0"] = bool(received["io"]["do0"])
        res["dout1"] = bool(received["io"]["do1"])
        res["pwmout0"] = int(received["io"]["po0"])
        res["general0"] = float(received["io"]["gn0"])
        res["general1"] = float(received["io"]["gn1"])
        res["button_a"] = bool(received["btn"]["a"])
        res["button_b"] = bool(received["btn"]["b"])
        res["button_c"] = bool(received["btn"]["c"])
        res["temperature"] = float(received["tmp"])
        res["pressure"] = float(received["pre"])
        res["brightness"] = int(received["bri"])
        res["is_response"] = bool(received["co"])
        res["time"] = self.current_time

        with self._condition:
            self._latest_msg = cast(M5ComDict, res)
            self._condition.notify_all()

    def _read(self) -> None:
        self._serial.reset_input_buffer()
        while not self._exit:
            if self._serial.in_waiting > 0:
                try:
                    self._read_line()
                except Exception as e:
                    print(f"An error occured in read thread: {e}")
            else:
                time.sleep(0.1)

    @property
    def reference_time(self) -> float:
        return self._reference_time

    @property
    def current_time(self) -> float:
        return time.time() - self.reference_time

    def send(self, data: bytes) -> None:
        self._serial.write(data)

    def send_data(self, data: Dict[str, Any]) -> bool:
        # TODO: Use exception
        try:
            json_data = json.dumps(data, ensure_ascii=False)
            self.send(bytes(json_data, "UTF-8"))
            return True
        except Exception as e:
            print(e)
            return False

    def wait_sync(self, sync_flg: bool) -> None:
        if sync_flg:

            def _predicate() -> bool:
                return self._latest_msg is not None and self._latest_msg["is_response"]

            with self._condition:
                self._condition.wait_for(_predicate)

    def get(self) -> M5ComDict:
        now = self.current_time

        def _predicate() -> bool:
            return self._latest_msg is not None and self._latest_msg["time"] > now

        with self._condition:
            self._condition.wait_for(_predicate)
            msg = self._latest_msg
            assert msg is not None
            return msg
