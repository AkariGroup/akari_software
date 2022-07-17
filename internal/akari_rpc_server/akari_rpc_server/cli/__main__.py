import argparse

from .. import server


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=51001)
    args = parser.parse_args()

    server.serve(args.port)


if __name__ == "__main__":
    main()
