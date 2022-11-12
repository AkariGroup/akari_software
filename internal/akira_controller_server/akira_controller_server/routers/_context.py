import dataclasses
from typing import Optional

from akari_client import AkariClient
from akira_controller_server.media import MediaController


@dataclasses.dataclass
class Context:
    akari_client: AkariClient
    media_controller: MediaController

    def close(self) -> None:
        self.media_controller.close()


_context: Optional[Context] = None


def get_context() -> Context:
    assert _context is not None, "context must be initialized before any use"
    return _context


def set_context(context: Context) -> None:
    global _context

    _context = context
