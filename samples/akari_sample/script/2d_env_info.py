#!/usr/bin/env python
# coding:utf-8

"""
Env info sample
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
            # 気圧の値はdata['pressure'][Pa]、気温の値はdata['temperature'][deg]、明るさの値はdata['brightness'](0-4096)に格納されている。
            # コマンドラインに取得した各値を表示する。
            print(
                "pressure: "
                + str(data["pressure"])
                + "[Pa] temperature: "
                + str(data["temperature"])
                + "[deg] brightness: "
                + str(data["brightness"])
            )
            # 1秒停止
            time.sleep(1)


if __name__ == "__main__":
    main()
