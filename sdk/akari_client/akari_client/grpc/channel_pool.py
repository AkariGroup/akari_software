import contextlib
import logging
import threading
from typing import Dict

import grpc

_logger = logging.getLogger(__name__)
_lock = threading.Lock()
_channels: Dict[str, grpc.Channel] = {}


def create_channel(stack: contextlib.ExitStack, endpoint: str) -> grpc.Channel:
    with _lock:
        c = _channels.get(endpoint)
        if c is not None:
            _logger.debug(f"Use existing channel for endpoint: '{endpoint}'")
            return c

        channel = stack.enter_context(grpc.insecure_channel(endpoint))
        _logger.debug(f"New channel for endpoint: '{endpoint}' created")
        _channels[endpoint] = channel
        return channel
