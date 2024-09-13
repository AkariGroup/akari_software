#!/usr/bin/env python3

import os
import argparse
from scservo_sdk import *  # Uses SCServo SDK library

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
        "-i",
        "--id",
        help="feetechサーボのidを指定します",
        default=1,
        type=int,
    )
    parser.add_argument(
        "-d",
        "--default_pos",
        help="セットするposの値を指定します",
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

    cur_baudrate = None
    for baudrate in badurate_list:
        # Set port baudrate
        if portHandler.setBaudRate(baudrate):
            print(f"シリアルポートをbaudrate: {baudrate} にセットしました。feetechサーボを探索します。")
        else:
            print(f"シリアルポートがbaudrate: {baudrate}に対応していません。スキップします。")
            continue
        scs_model_number, scs_comm_result, scs_error = packetHandler.ping(
                    portHandler, args.id
                )
        if scs_comm_result == COMM_SUCCESS and scs_error == 0:
            cur_baudrate = baudrate
            print(f"baudrate: {baudrate} にfeetechサーボID: {args.id}を発見しました。")
            break
    if cur_baudrate is None:
        print(f"[ERROR] サーボID: {args.id}が見つかりませんでした")
        return

    print()
    # EEPROM ROCK解除
    scs_comm_result, scs_error = packetHandler.write1ByteTxRx(
        portHandler, args.id, 55, 0
    )
    if scs_comm_result == COMM_SUCCESS:
        print(f"EEPROMロック解除しました。")
    else:
        print(f"[ERROR] EPROMロック解除に失敗しました。")
        return

    print("ENTERキーを入力すると、初期位置設定を開始します。")
    input()

    # 現在位置の取得
    retry_count = 0
    while True:
        try:
            cur_position, scs_comm_result, scs_error = packetHandler.read2ByteTxRx(
                portHandler, args.id, 56
            )
            if scs_comm_result == COMM_SUCCESS:
                print(f"現在位置: {cur_position}")
                break
            else:
                print("[ERROR] 現在位置の取得に失敗しました。id, Baudrate間違い、モータの接続間違いがないか確認してください。")
                return
        except:
            retry_count += 1
            if retry_count >= 5:
                print("[ERROR] 現在位置の取得に失敗しました。id, Baudrate間違い、モータの接続間違いがないか確認してください。")
                return
            print("    現在位置の取得をリトライします")
            pass

    time.sleep(0.5)
    # cur_offsetを0にリセット
    print(f"現在のオフセット値をリセットします。")
    scs_comm_result, scs_error = packetHandler.write2ByteTxRx(
        portHandler, args.id, 31, 0
    )
    time.sleep(0.5)
    # 現在位置の取得
    print()
    print(f"現在位置を再取得します。")
    retry_count = 0
    while True:
        try:
            cur_position, scs_comm_result, scs_error = packetHandler.read2ByteTxRx(
                portHandler, args.id, 56
            )
            if scs_comm_result == COMM_SUCCESS:
                print(f"現在位置: {cur_position}")
                break
            else:
                print("[ERROR] 現在位置の取得に失敗しました。id, Baudrate間違い、モータの接続間違いがないか確認してください。")
                return
        except:
            retry_count += 1
            if retry_count >= 5:
                print("[ERROR] 現在位置の取得に失敗しました。id, Baudrate間違い、モータの接続間違いがないか確認してください。")
                return
            print("    現在位置の取得をリトライします")
            pass

    time.sleep(0.5)
    diff = cur_position - args.default_pos
    offset = diff
    if offset > 4096:
        offset = offset % 4096
    if 4095 > offset > 2048:
        offset = 4096 - offset
    elif offset < 0:
        offset = 2048 - offset
    # 0点セット
    scs_comm_result, scs_error = packetHandler.write2ByteTxRx(
        # portHandler, args.id, 31, 0
        portHandler,
        args.id,
        31,
        offset,
    )
    if scs_comm_result == COMM_SUCCESS or COMM_RX_TIMEOUT:
        print(f"現在位置を{args.default_pos}にオフセットしました。")
    else:
        print("[ERROR] オフセットに失敗しました。id, Baudrate間違い、モータの接続間違いがないか確認してください。")
        return

    time.sleep(0.5)
    # EEPROM ROCK
    scs_comm_result, scs_error = packetHandler.write1ByteTxRx(
        portHandler, args.id, 55, 1
    )
    if scs_comm_result == COMM_SUCCESS:
        print(f"EEPROMをロックしました。")
    else:
        print(f"[ERROR] id {args.id}での接続に失敗しました。id, Baudrate間違い、モータの接続間違いがないか確認してください。")
        return
    portHandler.closePort()
    print()
    print(f"シリアルポートを再OPENします。")
    time.sleep(1.0)

    # Open port
    if portHandler.openPort():
        print("シリアルポートを開きました。")
    else:
        print("[ERROR] シリアルポートのOpenに失敗しました。")
        quit()

    # Set port baudrate
    if portHandler.setBaudRate(cur_baudrate):
        print(f"シリアルポートをbaudrate {cur_baudrate} にセットしました。")
    else:
        print("[ERROR] シリアルポートのbaudrateの変更に失敗しました。")
        quit()

    time.sleep(0.5)
    # 現在位置の取得
    for i in range(0, 3):
        cur_position, scs_comm_result, scs_error = packetHandler.read2ByteTxRx(
            portHandler, args.id, 56)
        if scs_comm_result != COMM_SUCCESS:
            if i == 2:
                print("[ERROR] %s" % packetHandler.getTxRxResult(scs_comm_result))
                print("------------------------")
                print("現在位置の取得に失敗しました")
                print("------------------------")
                break
            continue
        elif scs_error != 0:
            if i == 2:
                print("[ERROR] %s" % packetHandler.getRxPacketError(scs_error))
                print("------------------------")
                print("現在位置の取得に失敗しました")
                print("------------------------")
                break
            continue
        else:
            print(f"現在位置: {cur_position}")
            break
    # Close port
    portHandler.closePort()


if __name__ == "__main__":
    main()
