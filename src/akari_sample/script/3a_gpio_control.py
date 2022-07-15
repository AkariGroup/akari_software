#!/usr/bin/env python
# coding:utf-8

"""
GPIO control sample
Created on 2021/06/11
@author: Kazuya Yamamoto
"""


import time

from akari_controller.m5serial_server_py import M5SerialServer


def main() -> None:
    """
    メイン関数
    """
    # m5と通信するクラスを呼び出す
    m5 = M5SerialServer()

    print("Start!")
    # 2秒停止
    time.sleep(2)

    # アプリが終了されるまでループする。
    while True:
        # STEP1. dout0の出力をHiにする。
        print("STEP1. Set dout0 to Hi")
        # pin_idが0ならdout0
        pin_id = 0
        # valがFalseならLo,TrueならHi
        val = True
        # set_doutを実行
        result = m5.set_dout(pin_id, val)
        # 結果を出力
        print("Result: " + str(result))
        # 2秒停止
        time.sleep(2)
        print()

        # STEP2. dout1の出力をHiにする。
        print("STEP2. Set dout1 to Hi")
        # pin_idが1ならdout1
        pin_id = 1
        # valがFalseならLo,TrueならHi
        val = True
        # set_doutを実行
        result = m5.set_dout(pin_id, val)
        # 結果を出力
        print("Result: " + str(result))
        # 2秒停止
        time.sleep(2)
        print()

        # STEP3. pwmout0の出力をHiにする。
        print("STEP3. Set pwmout0 to 255")
        # pin_idが0ならpwmout0
        pin_id = 0
        # valがFalseならLo,TrueならHi
        pwmval = 255
        # set_pwmoutを実行
        result = m5.set_pwmout(pin_id, pwmval)
        # 結果を出力
        print("Result: " + str(result))
        # 2秒停止
        time.sleep(2)
        print()

        # STEP4. 出力ピンの現在値を表示(2cのサンプルと同様)
        print("STEP4. Display current output pin value")
        # M5からデータを取得
        data = m5.get()
        # dout0はdata['dout0'], dout1はdata['dout1'], pwmout0はdata['pwmout0']に
        # 結果が得られるので、それらをコマンドラインに表示。
        print(
            "dout0: "
            + str(int(data["dout0"]))
            + " dout1: "
            + str(int(data["dout1"]))
            + " pwmout0: "
            + str(data["pwmout0"])
        )
        # 1秒停止
        time.sleep(1)
        print()

        # STEP5. すべての出力をリセットにする。
        print("STEP5. Reset all output")
        # reset_alloutを実行
        result = m5.reset_allout()
        # 結果を出力
        print("Result: " + str(result))
        # 2秒停止
        time.sleep(2)
        print()

        # STEP6. 出力ピンの現在値を表示(2cのサンプルと同様)
        print("STEP6. Display current output pin value")
        # M5からデータを取得
        data = m5.get()
        # dout0はdata['dout0'], dout1はdata['dout1'], pwmout0はdata['pwmout0']に
        # 結果が得られるので、それらをコマンドラインに表示。
        print(
            "dout0: "
            + str(int(data["dout0"]))
            + " dout1: "
            + str(int(data["dout1"]))
            + " pwmout0: "
            + str(data["pwmout0"])
        )
        # 1秒停止
        time.sleep(1)
        print()

        # STEP7. set_alloutで全出力を同時に変更する。dout0:Hi dout1:Hi pwmout0:200
        print("STEP7. Set allout. dout0:Hi dout1:Hi pwmout0:200")
        # dout0_valがFalseならdout0がLo,TrueならHi
        dout0_val = True
        # dout1_valがFalseならdout1がLo,TrueならHi
        dout1_val = True
        # pwmout0_valでpwmout0の出力値を設定
        pwmout0_val = 200
        # set_alloutを実行
        result = m5.set_allout(dout0_val, dout1_val, pwmout0_val)
        # 結果を出力
        print("Result: " + str(result))
        # 2秒停止
        time.sleep(2)
        print()

        # STEP8. 出力ピンの現在値を表示(2cのサンプルと同様)
        print("STEP8. Display current output pin value")
        # M5からデータを取得
        data = m5.get()
        # dout0はdata['dout0'], dout1はdata['dout1'], pwmout0はdata['pwmout0']に
        # 結果が得られるので、それらをコマンドラインに表示。
        print(
            "dout0: "
            + str(int(data["dout0"]))
            + " dout1: "
            + str(int(data["dout1"]))
            + " pwmout0: "
            + str(data["pwmout0"])
        )
        # 1秒停止
        time.sleep(1)
        print()

        # STEP9. すべての出力を再度リセットにする。
        print("STEP9. Reset all output")
        # reset_alloutを実行
        result = m5.reset_allout()
        # 結果を出力
        print("Result: " + str(result))
        # 2秒停止
        time.sleep(2)
        print()

        print("Finish!")
        print()
        # 5秒停止
        time.sleep(5)


if __name__ == "__main__":
    main()
