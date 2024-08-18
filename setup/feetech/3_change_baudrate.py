#!/usr/bin/env python3

import os
import argparse
import time
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
        default="/dev/ttyACA0",
        type=str,
    )
    parser.add_argument(
        "-b",
        "--baudrate",
        help="変更したいBaudrateを指定します",
        default=500000,
        type=int,
    )
    parser.add_argument(
        "--id_pan",
        help="pan方向のfeetechサーボのidを指定します",
        default=1,
        type=int,
    )
    parser.add_argument(
        "--id_tilt",
        help="tilt方向のfeetechサーボのidを指定します",
        default=2,
        type=int,
    )

    args = parser.parse_args()

    if os.name == "nt":
        import msvcrt

    else:
        import sys, tty, termios

        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)

    try:
        baudrate_index = badurate_list.index(args.baudrate)
    except ValueError:
        print("このbaudrateは対応していません。")
        return

    portHandler = PortHandler(args.port)
    packetHandler = PacketHandler(protocol_end)

    # Open port
    if portHandler.openPort():
        print("シリアルポートを開きました。")
    else:
        print("[ERROR] シリアルポートのOpenに失敗しました。")
        quit()

    cur_baudrate = None
    print(f"STEP1: Panのサーボを探索し、IDを{args.changed_id_pan}に変更します。")
    for baudrate in badurate_list:
        # Set port baudrate
        portHandler.setBaudRate(baudrate)
        scs_model_number, scs_comm_result, scs_error = packetHandler.ping(
            portHandler, args.pan_id
        )
        if scs_comm_result == COMM_SUCCESS and scs_error == 0:
            cur_baudrate = baudrate
            print(
                f"baudrate: {baudrate} にfeetechサーボID: {args.pan_id}を発見しました。"
            )
            break
    if cur_baudrate is None:
        print(f"[ERROR] サーボID: {args.pan_id}が見つかりませんでした")
        return

    # EEPROM ROCK解除
    scs_comm_result, scs_error = packetHandler.write1ByteTxRx(
        portHandler, args.pan_id, 55, 0
    )
    if scs_comm_result == COMM_SUCCESS:
        print(f"EEPROMロック解除しました。")
    else:
        print(f"[ERROR] EPROMロック解除に失敗しました。")
        return

    # Baudrateの変更
    for i in range(0, 3):
        time.sleep(0.5)
        scs_comm_result, scs_error = packetHandler.write1ByteTxRx(
            portHandler, args.pan_id, 6, baudrate_index
        )
        if scs_comm_result == COMM_SUCCESS:
            print(
                f"PanのサーボのBaudrateを {badurate_list[baudrate_index]} に変更しました。"
            )
            break
        else:
            if i == 2:
                print(
                    "[ERROR] PanのサーボのBaudrateの変更に失敗しました。id間違い、モータの接続間違いがないか確認してください。"
                )
                return

    cur_baudrate = None
    print(f"STEP2: Tiltのサーボを探索し、IDを{args.changed_id_tilt}に変更します。")
    for baudrate in badurate_list:
        # Set port baudrate
        portHandler.setBaudRate(baudrate)
        scs_model_number, scs_comm_result, scs_error = packetHandler.ping(
            portHandler, args.tilt_id
        )
        if scs_comm_result == COMM_SUCCESS and scs_error == 0:
            cur_baudrate = baudrate
            print(
                f"baudrate: {baudrate} にfeetechサーボID: {args.tilt_id}を発見しました。"
            )
            break
    if cur_baudrate is None:
        print(f"[ERROR] サーボID: {args.tilt_id}が見つかりませんでした")
        return

    # EEPROM ROCK解除
    scs_comm_result, scs_error = packetHandler.write1ByteTxRx(
        portHandler, args.tilt_id, 55, 0
    )
    if scs_comm_result == COMM_SUCCESS:
        print(f"EEPROMロック解除しました。")
    else:
        print(f"[ERROR] EPROMロック解除に失敗しました。")
        return

    # Baudrateの変更
    for i in range(0, 3):
        time.sleep(0.5)
        scs_comm_result, scs_error = packetHandler.write1ByteTxRx(
            portHandler, args.tilt_id, 6, baudrate_index
        )
        if scs_comm_result == COMM_SUCCESS:
            print(
                f"TiltのサーボのBaudrateを {badurate_list[baudrate_index]} に変更しました。"
            )
            break
        else:
            if i == 2:
                print(
                    "[ERROR] TiltのサーボのBaudrateの変更に失敗しました。id間違い、モータの接続間違いがないか確認してください。"
                )
                return

    time.sleep(0.5)
    print()

    print("STEP3: 変更したbaudrateでpingを試します。")
    # Set port baudrate
    if portHandler.setBaudRate(args.baudrate):
        print(f"シリアルポートをbaudrate {args.baudrate} にセットしました。")
    else:
        print("[ERROR] シリアルポートのbaudrateの変更に失敗しました。")
        quit()

    pan_status = False
    tilt_status = False
    # Try to ping the Pan SCServo
    # Get SCServo model number
    for i in range(0, 3):
        scs_model_number, scs_comm_result, scs_error = packetHandler.ping(
            portHandler, args.id_pan
        )
        if scs_comm_result != COMM_SUCCESS:
            if i == 2:
                print("[ERROR] %s" % packetHandler.getTxRxResult(scs_comm_result))
                print("------------------------")
                print("Panのサーボのpingに失敗しました")
                print("------------------------")
                break
            continue
        elif scs_error != 0:
            if i == 2:
                print("[ERROR] %s" % packetHandler.getRxPacketError(scs_error))
                print("------------------------")
                print("Panのサーボのpingに失敗しました")
                print("------------------------")
                break
            continue
        else:
            print(
                "Panのサーボのpingに成功しました。 [ID:%03d]. モータモデル : %d"
                % (args.id_pan, scs_model_number)
            )
            # EEPROM ROCK
            scs_comm_result, scs_error = packetHandler.write1ByteTxRx(
                portHandler, args.id_pan, 55, 1
            )
            if scs_comm_result == COMM_SUCCESS:
                print(f"PanのサーボのEEPROMロックしました。")
                pan_status = True
            else:
                print(f"[ERROR] PanのサーボのEEPROMロックに失敗しました。")
                return
    # Try to ping the Tilt SCServo
    # Get SCServo model number
    for i in range(0, 3):
        scs_model_number, scs_comm_result, scs_error = packetHandler.ping(
            portHandler, args.id_tilt
        )
        if scs_comm_result != COMM_SUCCESS:
            if i == 2:
                print("[ERROR] %s" % packetHandler.getTxRxResult(scs_comm_result))
                print("------------------------")
                print("Tiltのサーボのpingに失敗しました")
                print("------------------------")
                break
            continue
        elif scs_error != 0:
            if i == 2:
                print("[ERROR] %s" % packetHandler.getRxPacketError(scs_error))
                print("------------------------")
                print("Tiltのサーボのpingに失敗しました")
                print("------------------------")
                break
            continue
        else:
            print(
                "TiltのモータのPingに成功しました。 [ID:%03d]. モータモデル : %d"
                % (args.id_tilt, scs_model_number)
            )
            # EEPROM ROCK
            scs_comm_result, scs_error = packetHandler.write1ByteTxRx(
                portHandler, args.id_tilt, 55, 1
            )
            if scs_comm_result == COMM_SUCCESS:
                print(f"EEPROMロックしました。")
                tilt_status = True
            else:
                print(f"[ERROR] EPROMロックに失敗しました。")
                return

    if pan_status and tilt_status:
        print("------------------------")
        print("Pan, Tiltのサーボのbaudrate変更OK!")
        print("------------------------")
    else:
        print("------------------------")
        print("Pan, Tiltのサーボのbaudrate変更失敗!")
        print("------------------------")

    # Close port
    portHandler.closePort()
    return


if __name__ == "__main__":
    main()
