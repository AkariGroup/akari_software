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

        print("Start!")
        # 2秒停止
        time.sleep(2)
        pos_x: int
        pos_y: int
        # アプリが終了されるまでループする。
        while True:
            # STEP1. '1.AKARI'を左上表示
            print("STEP1. display 1.AKARI at top left")
            # textは'1.AKARI'
            text = "1.AKARI"
            # pos_xは0-320で座標指定。0もしくはPositions.LEFTが左
            pos_x = Positions.LEFT
            # pos_yは0-240で座標指定。0もしくはPositions.TOPが上
            pos_y = Positions.TOP
            # 文字サイズは3
            size = 3
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

            # STEP2. '2.あかり'を中央に表示
            print("STEP2. display 2.あかり at middle center")
            text = "2.あかり"
            # pos_xはPositions.CENTERで左右中央
            pos_x = Positions.CENTER
            # pos_yはPositions.CENTERで上下中央
            pos_y = Positions.CENTER
            # 文字サイズは3
            size = 3
            # 文字色は赤
            text_color = Colors.RED
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

            # STEP3. '3.灯り'を右下揃えに表示
            print("STEP3. display 3.灯り at bottom right")
            # textは'3.灯り'
            text = "3.灯り"
            # pos_xはPositions.RIGHTで右揃え
            pos_x = Positions.RIGHT
            # pos_yはPositions.BOTTOMで下揃え
            pos_y = Positions.BOTTOM
            # 文字サイズは4
            size = 4
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
            # 文字サイズは2
            size = 2
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
            # 文字サイズは3
            size = 3
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

            # STEP.6 フォントを軽量内蔵フォントに変更する。
            print("STEP6. Change font")
            # dataをFalseにすることで、フォントを内蔵フォントに変更可能
            data = False
            m5.use_japanese_font(data)
            print("-> Set")
            print()

            # STEP7. 変更したフォントで'7.アカリ'を(50,170)にリフレッシュなしで重ねて表示
            print("STEP7. display 7.アカリ at (50,170) with new font")
            # textは'7.アカリ'
            text = "7.アカリ"
            # pos_xは50
            pos_x = 50
            # pos_yは170
            pos_y = 170
            # 文字サイズは4
            size = 4
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

            # STEP.8 フォントをデフォルトフォントに変更する。
            print("STEP8. Change font to default")
            # dataをTrueにすることで、フォントをデフォルトフォントに変更可能
            data = True
            m5.use_japanese_font(data)
            print("-> Set")
            # 2秒停止
            time.sleep(2)
            print()

            # STEP9. '9.灯'を中央に表示
            print("STEP9. display 9.灯 at middle center")
            # textは'9.灯'
            text = "9.灯"
            # pos_xはPositions.CENTERで左右中央
            pos_x = Positions.CENTER
            # pos_yはPositions.CENTERで上下中央
            pos_y = Positions.CENTER
            # 文字サイズは6
            size = 6
            # 文字色は白
            text_color = Colors.WHITE
            # 背景色は黒
            back_color = Colors.BLACK
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

            print("Finish!")
            print()
            # 5秒停止
            time.sleep(5)


if __name__ == "__main__":
    main()
