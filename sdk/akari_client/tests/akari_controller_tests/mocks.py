from typing import Any, Dict, List


class MockDynamixelCommunicator:
    def __init__(self, n_devices: int, n_address: int) -> None:
        self.simulate_error: bool = False

        self._memory: List[List[int]] = [
            [0 for x in range(n_address)] for y in range(n_devices)
        ]

    def read(self, device_id: int, address: int, length: int) -> int:
        if self.simulate_error:
            raise RuntimeError()

        # NOTE: In order to check if length is passed to read/write functions properly,
        # add/sub length to/from value when loading/storing memory
        return self._memory[device_id][address] + (length - 1)

    def write(self, device_id: int, address: int, length: int, value: int) -> None:
        if self.simulate_error:
            raise RuntimeError()

        self._memory[device_id][address] = value - (length - 1)


class MockFeetechCommunicator:
    def __init__(self, n_devices: int, n_address: int) -> None:
        self.simulate_error: bool = False

        self._memory: List[List[int]] = [
            [0 for x in range(n_address)] for y in range(n_devices)
        ]

    def read(self, device_id: int, address: int, length: int) -> int:
        if self.simulate_error:
            raise RuntimeError()

        # NOTE: In order to check if length is passed to read/write functions properly,
        # add/sub length to/from value when loading/storing memory
        return self._memory[device_id][address] + (length - 1)

    def write(self, device_id: int, address: int, length: int, value: int) -> None:
        if self.simulate_error:
            raise RuntimeError()

        self._memory[device_id][address] = value - (length - 1)


class MockM5Communicator:
    def __init__(self) -> None:
        pass

    def start(self) -> None:
        pass

    def stop(self) -> None:
        pass

    def send_data(self, data: Dict[str, Any], sync: bool = True) -> None:
        pass

    def get(self) -> Any:
        raise NotImplementedError()
