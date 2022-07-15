#!/usr/bin/env python
# coding:utf-8

"""
Reset M5 sample
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
        print("Reset M5")
        # reset_m5を実行
        result = m5.reset_m5()
        # 結果を出力
        print("Result: " + str(result))
        # 5秒停止
        time.sleep(5)


if __name__ == "__main__":
    main()
