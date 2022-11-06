import argparse
import contextlib

from akari_client import AkariClient

from .. import media, server
from ..routers._context import Context, set_context


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=52001)
    args = parser.parse_args()

    with contextlib.ExitStack() as stack:
        client = stack.enter_context(AkariClient())
        context = Context(
            akari_client=client,
            media_controller=media.MediaController(),
        )
        stack.enter_context(contextlib.closing(context))
        set_context(context)
        server.serve("0.0.0.0", args.port)


if __name__ == "__main__":
    main()
