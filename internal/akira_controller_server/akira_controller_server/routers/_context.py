import dataclasses
from typing import Optional

from akari_client import AkariClient


@dataclasses.dataclass
class Context:
    akari_client: AkariClient


_context: Optional[Context] = None


def get_context() -> Context:
    assert _context is not None, "context must be initialized before any use"
    return _context


def set_context(context: Context) -> None:
    global _context

    _context = context
