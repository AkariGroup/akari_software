#!/usr/bin/env python
# coding:utf-8

"""
GPIO input sample
Created on 2021/06/11
@author: Kazuya Yamamoto
"""

import time

from akari_client import AkariClient


def main() -> None:
    """
    メイン関数
    """
    with AkariClient() as akari:
        # m5と通信するクラスを呼び出す
        m5 = akari.m5stack

        print("Start!")
        # 2秒停止
        time.sleep(2)

        # アプリが終了されるまで、データ取得を実行し続ける。
        while True:
            # M5からデータを取得
            data = m5.get()
            # din0はdata['din0'], din1はdata['din1'], ain0はdata['ain0']に結果が得られるので、それらをコマンドラインに表示。
            print(
                "din0: "
                + str(int(data["din0"]))
                + " din1: "
                + str(int(data["din1"]))
                + " ain0: "
                + str(data["ain0"])
            )
            # 1秒停止
            time.sleep(1)


if __name__ == "__main__":
    main()
