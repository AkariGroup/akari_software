#!/usr/bin/env python
# coding:utf-8

"""
GPIO output sample
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

    # アプリが終了されるまで、データ取得を実行し続ける。
    while True:
        # M5からデータを取得
        data = m5.get()
        # dout0はdata['dout0'], dout1はdata['dout1'], pwmout0はdata['pwmout0']
        # に結果が得られるので、それらをコマンドラインに表示。
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


if __name__ == "__main__":
    main()
