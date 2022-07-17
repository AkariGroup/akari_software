#!/usr/bin/env python
# coding:utf-8

"""
Reset M5 sample
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

        # アプリが終了されるまでループする。
        while True:
            print("Reset M5")
            # reset_m5を実行
            m5.reset_m5()
            # 結果を出力
            print("-> Reset")
            # 5秒停止
            time.sleep(5)


if __name__ == "__main__":
    main()
