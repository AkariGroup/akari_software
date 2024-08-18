#!/usr/bin/env python3

import os
import argparse
from scservo_sdk import *  # Uses SCServo SDK library

# Control table address
ADDR_SCS_TORQUE_ENABLE = 40
ADDR_SCS_GOAL_POSITION = 42
ADDR_SCS_GOAL_SPEED = 46

# Default setting
protocol_end = 0  # SCServo bit end(STS/SMS=0, SCS=1)
motor_velocity = 300


def main() -> None:
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p",
        "--port",
        help="シリアルポートを指定します",
        default="/dev/ttyACA0",
        type=str,
    )
    parser.add_argument(
        "-b",
        "--baudrate",
        help="Baudrateを指定します",
        default=500000,
        type=int,
    )
    parser.add_argument(
        "-m",
        "--move_pos",
        help="移動先のfeetechサーボのposを指定します",
        default=2048,
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

    # Set port baudrate
    if portHandler.setBaudRate(args.baudrate):
        print(f"シリアルポートをbaudrate {args.baudrate} にセットしました。")
    else:
        print("[ERROR] シリアルポートのbaudrateの変更に失敗しました。")
        quit()

    for id in range(1, 3):
        cur_position, scs_comm_result, scs_error = packetHandler.read2ByteTxRx(
            portHandler, id, 56
        )
        if scs_comm_result == COMM_SUCCESS:
            print(f"id: {id}, 現在位置: {cur_position}")
        else:
            print("[ERROR] 現在位置の取得に失敗しました。id, Baudrate間違い、モータの接続間違いがないか確認してください。")
            return

    print()
    print("ENTERキーを入力すると、全軸サーボONします。")
    input()

    for id in range(1, 3):
        # サーボON
        scs_comm_result, scs_error = packetHandler.write1ByteTxRx(
            portHandler, id, ADDR_SCS_TORQUE_ENABLE, 1
        )
        if scs_comm_result != COMM_SUCCESS:
            print(f"[ERROR] ID: {id} のサーボONに失敗しました。ID, Baudrateが正しいか、接続が正しいか確認してください。")
            print("[ERROR] %s" % packetHandler.getTxRxResult(scs_comm_result))
            return
        elif scs_error != 0:
            print(f"[ERROR] ID: {id} のサーボONに失敗しました。ID, Baudrateが正しいか、接続が正しいか確認してください。")
            print("[ERROR] %s" % packetHandler.getRxPacketError(scs_error))
            return

    print()
    print(f"ENTERキーを入力すると、サーボが{args.move_pos}に動きます。")
    input()

    for id in range(1, 3):
        # 速度を落とす
        scs_comm_result, scs_error = packetHandler.write2ByteTxRx(
            portHandler, id, ADDR_SCS_GOAL_SPEED, motor_velocity
        )
        # 0pos
        scs_comm_result, scs_error = packetHandler.write2ByteTxRx(
            portHandler, id, ADDR_SCS_GOAL_POSITION, args.move_pos
        )
        if scs_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(scs_comm_result))
        elif scs_error != 0:
            print("%s" % packetHandler.getRxPacketError(scs_error))

    print()
    print("")
    print("ENTERキーを入力するとサーボOFFします。")
    input()

    for id in range(1, 3):
        # サーボOFF
        scs_comm_result, scs_error = packetHandler.write1ByteTxRx(
            portHandler, id, ADDR_SCS_TORQUE_ENABLE, 0
        )
        if scs_comm_result == COMM_SUCCESS:
            print(f"id:{id} サーボOFFしました。")
        else:
            print("[ERROR] %s" % packetHandler.getTxRxResult(scs_comm_result))
        if scs_error != 0:
            print("[ERROR] %s" % packetHandler.getRxPacketError(scs_error))

    print("------------------------")
    print("動作完了！")
    print("------------------------")
    # Close port
    portHandler.closePort()


if __name__ == "__main__":
    main()
