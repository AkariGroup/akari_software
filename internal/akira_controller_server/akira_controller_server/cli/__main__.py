import argparse

from akari_client import AkariClient

from .. import server
from ..routers._context import Context, set_context


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=51001)
    args = parser.parse_args()

    with AkariClient() as client:
        context = Context(
            akari_client=client,
        )
        set_context(context)
        server.serve("0.0.0.0", args.port)


if __name__ == "__main__":
    main()
