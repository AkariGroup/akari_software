#!/usr/bin/env python3

import os
import time
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
        default="/dev/ttyACA0",
        type=str,
    )
    parser.add_argument(
        "-s",
        "--search_id",
        help="最大で探索するサーボID",
        default=10,
        type=int,
    )
    parser.add_argument(
        "-c",
        "--changed_id",
        help="変更後のfeetechサーボのidを指定します",
        default=100,
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
        portHandler.setBaudRate(baudrate):
        for id in range(0, args.search_id):
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
                for i in range(0, 3):
                    time.sleep(0.5)
                    scs_comm_result, scs_error = packetHandler.write1ByteTxRx(
                        portHandler, id, 5, args.changed_id
                    )
                    if scs_comm_result == COMM_SUCCESS or COMM_RX_TIMEOUT:
                        print(f"サーボのidを {id} から {args.changed_id} に変更しました。")
                        break
                    else:
                        if i == 2:
                            print(
                                "[ERROR] サーボのidの変更に失敗しました。current_idの間違い、モータの接続間違いがないか確認してください。"
                            )
                            return

                time.sleep(0.5)
                print()
                print("変更したidでpingを試します。")

                # Try to ping the SCServo
                # Get SCServo model number
                for i in range(0, 3):
                    scs_model_number, scs_comm_result, scs_error = packetHandler.ping(
                        portHandler, args.changed_id
                    )
                    if scs_comm_result != COMM_SUCCESS:
                        if i == 2:
                            print("[ERROR] %s" % packetHandler.getTxRxResult(scs_comm_result))
                            print("------------------------")
                            print("pingに失敗しました")
                            print("------------------------")
                            break
                        continue
                    elif scs_error != 0:
                        if i == 2:
                            print("[ERROR] %s" % packetHandler.getRxPacketError(scs_error))
                            print("------------------------")
                            print("pingに失敗しました")
                            print("------------------------")
                            break
                        continue
                    else:
                        print(
                            "Pingに成功しました。 [ID:%03d]. モータモデル : %d"
                            % (args.changed_id, scs_model_number)
                        )
                        # EEPROM ROCK
                        scs_comm_result, scs_error = packetHandler.write1ByteTxRx(
                            portHandler, args.changed_id, 55, 1
                        )
                        if scs_comm_result == COMM_SUCCESS:
                            print(f"EEPROMロックしました。")
                        else:
                            print(f"[ERROR] EPROMロックに失敗しました。")
                            return
                        print("------------------------")
                        print("idの仮変更OK!")
                        print("------------------------")
                # Close port
                portHandler.closePort()
                return


if __name__ == "__main__":
    main()
