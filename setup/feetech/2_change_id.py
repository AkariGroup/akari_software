#!/usr/bin/env python3

import os
import time
import argparse
from scservo_sdk import *  # Uses SCServo SDK library

protocol_end = 0  # SCServo bit end(STS/SMS=0, SCS=1)
badurate_list = [1000000, 500000, 250000, 128000, 115200, 76800, 57600, 38400]
MAX_TRY_TIME = 3

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
        "--changed_id_tilt",
        help="変更後のtilt方向のfeetechサーボのidを指定します",
        default=2,
        type=int,
    )
    parser.add_argument(
        "--cur_id_pan",
        help="変更前のpan方向のfeetechサーボのidを指定します",
        default=100,
        type=int,
    )
    parser.add_argument(
        "--changed_id_pan",
        help="変更後のpan方向のfeetechサーボのidを指定します",
        default=1,
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

    baudrate_pan = None
    baudrate_tilt = None
    print(f"STEP1: Tiltのサーボを探索し、IDを{args.changed_id_tilt}に変更します。")
    is_changed = False
    for baudrate in badurate_list:
        # Set port baudrate
        portHandler.setBaudRate(baudrate)
        for id in range(0,100):
            if is_changed:
                break
            scs_model_number, scs_comm_result, scs_error = packetHandler.ping(
                portHandler, id
            )
            if scs_comm_result == COMM_SUCCESS and scs_error == 0:
                print("------------------------------------------------------------")
                print(
                    "Feetechサーボが見つかりました。Baudrate: %d, ID:%03d, モデル名:%d"
                    % (baudrate, id, scs_model_number)
                )
                print()
                # EEPROM ROCK解除
                scs_comm_result, scs_error = packetHandler.write1ByteTxRx(
                    portHandler, id, 55, 0
                )
                if scs_comm_result == COMM_SUCCESS:
                    print(f"EEPROMロック解除しました。")
                else:
                    print(f"[ERROR] EPROMロック解除に失敗しました。")
                    return

                # IDの変更
                while not is_changed:
                    try_time = 0
                    time.sleep(0.5)
                    scs_comm_result, scs_error = packetHandler.write1ByteTxRx(
                        portHandler, id, 5, args.changed_id_tilt
                    )
                    if scs_comm_result == COMM_SUCCESS or COMM_RX_TIMEOUT:
                        is_changed = True
                        baudrate_tilt = baudrate
                        print(f"サーボのidを {id} から {args.changed_id_tilt} に変更しました。")
                    else:
                        try_time += 1
                        if try_time >= MAX_TRY_TIME:
                            print(
                                "[ERROR] サーボのidの変更に失敗しました。current_idの間違い、モータの接続間違いがないか確認してください。"
                            )
                            return
    if not is_changed:
        print(f"[ERROR] Tiltのサーボが見つかりませんでした。")
        print(f"[ERROR] Tiltのサーボのコネクタが接続されているか確認してください。")
        return

    time.sleep(0.5)
    print()
    print("STEP2: Panのサーボを探索し、IDを1に変更します。")
    is_changed = False
    for baudrate in badurate_list:
        if is_changed:
            break
        # Set port baudrate
        portHandler.setBaudRate(baudrate)
        scs_model_number, scs_comm_result, scs_error = packetHandler.ping(
            portHandler, args.cur_id_pan
        )
        if scs_comm_result == COMM_SUCCESS and scs_error == 0:
            print("------------------------------------------------------------")
            print(
                "Feetechサーボが見つかりました。Baudrate: %d, ID:%03d, モデル名:%d"
                % (baudrate, args.cur_id_pan, scs_model_number)
            )
            print()
            # EEPROM ROCK解除
            scs_comm_result, scs_error = packetHandler.write1ByteTxRx(
                portHandler, args.cur_id_pan, 55, 0
            )
            if scs_comm_result == COMM_SUCCESS:
                print(f"EEPROMロック解除しました。")
            else:
                print(f"[ERROR] EPROMロック解除に失敗しました。")
                return

            # IDの変更
            while not is_changed:
                try_time = 0
                time.sleep(0.5)
                scs_comm_result, scs_error = packetHandler.write1ByteTxRx(
                    portHandler, args.cur_id_pan, 5, args.changed_id_pan
                )
                if scs_comm_result == COMM_SUCCESS or COMM_RX_TIMEOUT:
                    print(f"サーボのidを {args.cur_id_pan} から {args.changed_id_pan} に変更しました。")
                    baudrate_pan = baudrate
                    is_changed = True
                    break
                else:
                    try_time += 1
                    if try_time >= MAX_TRY_TIME:
                        print(
                            "[ERROR] サーボのidの変更に失敗しました。current_idの間違い、モータの接続間違いがないか確認してください。"
                        )
                        return
    if not is_changed:
        print(f"[ERROR] Panのサーボが見つかりませんでした。")
        print(f"[ERROR] Panのサーボのidを'1_temp_change_id.py'で{args.cur_id_pan}に変更済みか確認してください。")
        return

    time.sleep(0.5)
    print()
    print("STEP3: 変更したidでpingを試します。")
    pan_status = False
    tilt_status = False
    # Try to ping the Pan SCServo
    # Get SCServo model number
    portHandler.setBaudRate(baudrate_pan)
    for i in range(0, MAX_TRY_TIME):
        scs_model_number, scs_comm_result, scs_error = packetHandler.ping(
            portHandler, args.changed_id_pan
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
                % (args.changed_id_pan, scs_model_number)
            )
            # EEPROM ROCK
            scs_comm_result, scs_error = packetHandler.write1ByteTxRx(
                portHandler, args.changed_id_pan, 55, 1
            )
            if scs_comm_result == COMM_SUCCESS:
                print(f"PanのサーボのEEPROMロックしました。")
                pan_status = True
                break
            else:
                print(f"[ERROR] PanのサーボのEEPROMロックに失敗しました。")
                return
    # Try to ping the Tilt SCServo
    # Get SCServo model
    portHandler.setBaudRate(baudrate_tilt)
    for i in range(0, MAX_TRY_TIME):
        scs_model_number, scs_comm_result, scs_error = packetHandler.ping(
            portHandler, args.changed_id_tilt
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
                "TiltのサーボのPingに成功しました。 [ID:%03d]. モータモデル : %d"
                % (args.changed_id_tilt, scs_model_number)
            )
            # EEPROM ROCK
            scs_comm_result, scs_error = packetHandler.write1ByteTxRx(
                portHandler, args.changed_id_tilt, 55, 1
            )
            if scs_comm_result == COMM_SUCCESS:
                print(f"TiltのサーボのEEPROMロックしました。")
                tilt_status = True
                break
            else:
                print(f"[ERROR] TiltのサーボのEPROMロックに失敗しました。")
                return
    if pan_status and tilt_status:
        print("------------------------")
        print("Pan, Tiltのサーボidの変更OK!")
        print("------------------------")
    else:
        print("------------------------")
        print("Pan, Tiltのサーボidの変更失敗!")
        print("------------------------")

    # Close port
    portHandler.closePort()
    return


if __name__ == "__main__":
    main()
