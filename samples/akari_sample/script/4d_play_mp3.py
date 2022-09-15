#!/usr/bin/env python
# coding:utf-8

"""
Display image sample
Created on 2021/06/11
@author: Kazuya Yamamoto
"""

import time

from akari_client import AkariClient
from akari_client.position import Positions


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

        # STEP1. M5のSDカード内のmp3'/mp3/hello.mp3'を再生
        print("STEP1. Play 'hello.mp3' in SD")
        # filepathでM5のSDカード内の音源のパスを指定
        filepath = "/mp3/hello.mp3"
        # play_mp3を実行
        m5.play_mp3(filepath)
        print("-> Set")
        # 2秒停止
        time.sleep(2)
        print()

        # STEP2. M5のSDカード内のmp3'/mp3/beep.mp3'を再生
        print("STEP2. Play 'beep.mp3' in SD")
        # filepathでM5のSDカード内の音源のパスを指定
        filepath = "/mp3/beep.mp3"
        # play_mp3を実行
        m5.play_mp3(filepath)
        print("-> Set")
        # 2秒停止
        time.sleep(2)
        print()

        # STEP3. mp3の再生を停止
        print("STEP3. Stop playing mp3")
        # stop_mp3を実行
        m5.stop_mp3()
        print("-> Set")
        # 2秒停止
        time.sleep(2)
        print()

if __name__ == "__main__":
    main()
