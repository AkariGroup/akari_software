#!/usr/bin/env python
# coding:utf-8

"""
Display color sample
Created on 2021/06/11
@author: Kazuya Yamamoto
"""


import time
import random

from akari_controller import AkariClient
from akari_controller.color import Colors, Color


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

        color: Color
        # アプリが終了されるまでループする。
        while True:
            # STEP1. ディスプレイの背景色を白にする
            print("STEP1. Set display color to white")
            # colorで'white'を指定
            color = Colors.WHITE
            # set_display_colorを実行
            m5.set_display_color(color)
            # 結果を出力
            print("-> Set")
            # 2秒停止
            time.sleep(2)
            print()

            # STEP2. ディスプレイの背景色を赤にする
            print("STEP2. Set display color to red")
            # colorで'red'を指定
            color = Colors.RED
            # set_display_colorを実行
            m5.set_display_color(color)
            # 結果を出力
            print("-> Set")
            # 2秒停止
            time.sleep(2)
            print()

            # STEP3. ディスプレイの背景色を青にする
            print("STEP3. Set display color to blue")
            # colorで'blue'を指定
            color = Colors.BLUE
            # set_display_colorを実行
            m5.set_display_color(color)
            # 結果を出力
            print("-> Set")
            # 2秒停止
            time.sleep(2)
            print()

            # STEP4. ディスプレイの背景色を紫にする
            print("STEP4. Set display color to magenta")
            # colorで'magenta'を指定
            color = Colors.MAGENTA
            # set_display_colorを実行
            m5.set_display_color(color)
            # 結果を出力
            print("-> Set")
            # 2秒停止
            time.sleep(2)
            print()

            # STEP5. ディスプレイの背景色をランダム色にする
            print("STEP5. Set display color to a random color")
            # colorを生成
            color = Color(
                red=random.randint(0, 255),
                green=random.randint(0, 255),
                blue=random.randint(0, 255),
            )
            # set_display_colorを実行
            m5.set_display_color(color)
            # 結果を出力
            print(f"-> Set (Color: {color})")
            # 2秒停止
            time.sleep(2)
            print()

            # STEP6. ディスプレイの背景色を黒にする
            print("STEP6. Set display color to black")
            # colorで'black'を指定
            color = Colors.BLACK
            # set_display_colorを実行
            m5.set_display_color(color)
            # 結果を出力
            print("-> Set")
            # 2秒停止
            time.sleep(2)
            print()

            print("Finish!")
            print()
            # 5秒停止
            time.sleep(5)


if __name__ == "__main__":
    main()
