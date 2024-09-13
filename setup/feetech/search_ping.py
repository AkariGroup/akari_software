#!/usr/bin/env python3

import os
import argparse
from scservo_sdk import *  # Uses SCServo SDK library

# Default setting
SCS_MOVING_STATUS_THRESHOLD = 20  # SCServo moving status threshold
protocol_end = 0  # SCServo bit end(STS/SMS=0, SCS=1)
badurate_list = [1000000, 500000, 250000, 128000, 115200, 76800, 57600, 38400]


def main() -> None:
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p",
        "--port",
        help="シリアルポートを指定します",
        default="/dev/ttyAMA0",
        type=str,
    )
    parser.add_argument(
        "-s",
        "--search_id",
        help="最大で探索するサーボID",
        default=10,
        type=int,
    )
    args = parser.parse_args()

    if os.name == "nt":
        import msvcrt

    else:
        import sys, tty, termios

        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)

    portHandler = PortHandler(args.port)
    packetHandler = PacketHandler(protocol_end)

    # Open port
    if portHandler.openPort():
        print("シリアルポートを開きました。")
    else:
        print("[ERROR] シリアルポートのOpenに失敗しました。")
        quit()

    for baudrate in badurate_list:
        # Set port baudrate
        if portHandler.setBaudRate(baudrate):
            print(f"シリアルポートをbaudrate: {baudrate} にセットしました。feetechサーボを探索します。")
        else:
            print(f"シリアルポートがbaudrate: {baudrate}に対応していません。スキップします。")

        for id in range(0, args.search_id + 1):
            scs_model_number, scs_comm_result, scs_error = packetHandler.ping(
                portHandler, id
            )
            if scs_comm_result == COMM_SUCCESS and scs_error == 0:
                print("------------------------------------------------------------")
                print(
                    "Feetechサーボが見つかりました。Baudrate: %d, ID:%03d, モデル名:%d"
                    % (baudrate, id, scs_model_number)
                )
                print("------------------------------------------------------------")

    print(f"スキャンが完了しました。")
    # Close port
    portHandler.closePort()


if __name__ == "__main__":
    main()
