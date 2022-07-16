#!/usr/bin/env python
# coding:utf-8

"""
Button sample
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

    # コマンドラインに'Press button!'と表示
    print("Press button!")

    # アプリが終了されるまで、データ取得を実行し続ける。
    while True:
        # M5からデータを取得
        data = m5.get()
        # ボタンAが押されているとdata['button_a']がTrue。コマンドラインに'Button A pressed!'と表示される。
        if data["button_a"]:
            print("Button A pressed!")
        # ボタンBが押されているとdata['button_b']がTrue。コマンドラインに'Button B pressed!'と表示される。
        if data["button_b"]:
            print("Button B pressed!")
        # ボタンCが押されているとdata['button_c']がTrue。コマンドラインに'Button C pressed!'と表示される。
        if data["button_c"]:
            print("Button C pressed!")
        # 0.1秒停止
        time.sleep(0.1)


if __name__ == "__main__":
    main()
