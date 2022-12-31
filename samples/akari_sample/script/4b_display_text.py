#!/usr/bin/env python
# coding:utf-8

"""
Display text sample
Created on 2021/06/11
@author: Kazuya Yamamoto
"""

import time

from akari_client import AkariClient
from akari_client.color import Colors
from akari_client.position import Positions

def main() -> None:
    """
    メイン関数
    """
    with AkariClient() as akari:
        # m5と通信するクラスを呼び出す
        m5 = akari.m5stack
        pos_x: int
        pos_y: int
        print("Start!")
        # 2秒停止
        time.sleep(2)
        # アプリが終了されるまでループする。
        while True:

            color = Colors.RED
            m5.set_display_color(color)
            # STEP1. '1.AKARI'を左上表示
            print("STEP1. display 1.AKARI at top left")
            # textは'1.AKARI'
            text = "1.AKARI"
            # pos_xは0-320で座標指定。0もしくはPositions.LEFTで左
            pos_x = Positions.LEFT
            # pos_yは0-240で座標指定。0もしくはPositions.TOPで上
            pos_y = Positions.TOP
            # 文字サイズは5
            size = 5
            # 文字色は黒
            text_color = Colors.BLACK
            # 背景色は白
            back_color = Colors.WHITE
            # 背景全体をリセット
            refresh = True
            # set_display_textを実行
            m5.set_display_text(
                text, pos_x, pos_y, size, text_color, back_color, refresh
            )
            print("-> Set")
            # 2秒停止
            time.sleep(2)
            print()

            # STEP2. '2.あかり'を中央に表示。位置、サイズ、文字色はデフォルト
            # 文字色、背景色はSTEP.1と同様、文字サイズは5、背景リセットはTrueとなる。
            print("STEP2. display 2.あかり at middle center")
            text = "2.あかり"
            # set_display_textを実行
            m5.set_display_text(text)
            print("-> Set")
            # 2秒停止
            time.sleep(2)
            print()

            # STEP3. '3.灯り'を右下揃えに表示
            print("STEP3. display 3.灯り at bottom right")
            # textは'3.灯り'
            text = "3.灯り"
            # pos_xはPositions.RIGHTで右揃え
            pos_x = Positions.RIGHT
            # pos_yはPositions.BOTTOMで下揃え
            pos_y = Positions.BOTTOM
            # 文字サイズは7
            size = 7
            # 文字色は白
            text_color = Colors.WHITE
            # 背景色は緑
            back_color = Colors.GREEN
            # 背景全体をリセット
            refresh = True
            # set_display_textを実行
            m5.set_display_text(
                text, pos_x, pos_y, size, text_color, back_color, refresh
            )
            print("-> Set")
            # 2秒停止
            time.sleep(2)
            print()

            # STEP4. '4.アカリ'を(50,40)に表示
            print("STEP4. display 4.アカリ at (50,40)")
            # textは'4.アカリ'
            text = "4.アカリ"
            # pos_xは60
            pos_x = 50
            # pos_yは40
            pos_y = 40
            # 文字サイズは3
            size = 3
            # 文字色は青
            text_color = Colors.BLUE
            # 背景色は黄
            back_color = Colors.YELLOW
            # 背景全体をリセット
            refresh = True
            # set_display_textを実行
            m5.set_display_text(
                text, pos_x, pos_y, size, text_color, back_color, refresh
            )
            print("-> Set")
            # 2秒停止
            time.sleep(2)
            print()

            # STEP5. '5.アカリ'を(50,100)に背景リフレッシュなしで重ねて表示
            print("STEP5. display 5.アカリ at (50,100) without background refresh")
            # textは'5.アカリ'
            text = "5.アカリ"
            # pos_xは50
            pos_x = 50
            # pos_yは40
            pos_y = 100
            # 文字サイズは5
            size = 5
            # 文字色は黒
            text_color = Colors.BLACK
            # 背景色は紫
            back_color = Colors.MAGENTA
            # refreshをFalseにすることで前の背景表示を消さずに追記できる。
            refresh = False
            # set_display_textを実行
            m5.set_display_text(
                text, pos_x, pos_y, size, text_color, back_color, refresh
            )
            print("-> Set")
            # 2秒停止
            time.sleep(2)
            print()

            # STEP6. '6.アカリ'を(50,170)にリフレッシュなしで重ねて表示
            print("STEP6. display 6.アカリ at (50,170) without background refresh")
            # textは'6.アカリ'
            text = "6.アカリ"
            # pos_xは50
            pos_x = 50
            # pos_yは170
            pos_y = 170
            # 文字サイズは3
            size = 3
            # 文字色はピンク
            text_color = Colors.PINK
            # 背景色は灰
            back_color = Colors.DARKGREY
            # refreshをFalseにすることで前の表示を消さずに追記できる。
            refresh = False
            # set_display_textを実行
            m5.set_display_text(
                text, pos_x, pos_y, size, text_color, back_color, refresh
            )
            print("-> Set")
            # 2秒停止
            time.sleep(2)
            print()

            # STEP7. '7.灯'を中央に表示
            print("STEP7. display 7.灯 at middle center")
            # textは'7.灯'
            text = "7.灯"
            # 文字サイズは11
            size = 11
            # 文字色は白
            text_color = Colors.WHITE
            # 背景色は黒
            back_color = Colors.BLACK
            # set_display_textを実行
            # pos_x,pos_yのみデフォルト引数を使用
            m5.set_display_text(
                text, size=size)
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
