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
        _pos_x: int
        _pos_y: int
        print("Start!")
        # 2秒停止
        time.sleep(2)
        # アプリが終了されるまでループする。
        while True:
            # STEP1. '1.AKARI'を左上表示
            print("STEP1. display 1.AKARI at top left")
            # _textは'1.AKARI'
            _text = "1.AKARI"
            # _pos_xは0-320で座標指定。0もしくはPositions.LEFTで左
            _pos_x = Positions.LEFT
            # _pos_yは0-240で座標指定。0もしくはPositions.TOPで上
            _pos_y = Positions.TOP
            # 文字サイズは3
            _size = 3
            # 文字色は黒
            _text_color = Colors.BLACK
            # 背景色は白
            _back_color = Colors.WHITE
            # 背景全体をリセット
            _refresh = True
            # set_display_textを実行
            m5.set_display_text(
                _text, _pos_x, _pos_y, _size, _text_color, _back_color, _refresh
            )
            print("-> Set")
            # 2秒停止
            time.sleep(2)
            print()

            # STEP2. '2.あかり'を中央に表示。位置、サイズ、文字色はデフォルト
            # デフォルト引数では文字色は黒、背景色は白、文字サイズは3、背景リセットはTrueとなる。
            print("STEP2. display 2.あかり at middle center")
            _text = "2.あかり"
            # set_display_textを実行
            m5.set_display_text(_text)
            print("-> Set")
            # 2秒停止
            time.sleep(2)
            print()

            # STEP3. '3.灯り'を右下揃えに表示
            print("STEP3. display 3.灯り at bottom right")
            # _textは'3.灯り'
            _text = "3.灯り"
            # _pos_xはPositions.RIGHTで右揃え
            _pos_x = Positions.RIGHT
            # _pos_yはPositions.BOTTOMで下揃え
            _pos_y = Positions.BOTTOM
            # 文字サイズは4
            _size = 4
            # 文字色は白
            _text_color = Colors.WHITE
            # 背景色は緑
            _back_color = Colors.GREEN
            # 背景全体をリセット
            _refresh = True
            # set_display_textを実行
            m5.set_display_text(
                _text, _pos_x, _pos_y, _size, _text_color, _back_color, _refresh
            )
            print("-> Set")
            # 2秒停止
            time.sleep(2)
            print()

            # STEP4. '4.アカリ'を(50,40)に表示
            print("STEP4. display 4.アカリ at (50,40)")
            # _textは'4.アカリ'
            _text = "4.アカリ"
            # _pos_xは60
            _pos_x = 50
            # _pos_yは40
            _pos_y = 40
            # 文字サイズは2
            _size = 2
            # 文字色は青
            _text_color = Colors.BLUE
            # 背景色は黄
            _back_color = Colors.YELLOW
            # 背景全体をリセット
            _refresh = True
            # set_display_textを実行
            m5.set_display_text(
                _text, _pos_x, _pos_y, _size, _text_color, _back_color, _refresh
            )
            print("-> Set")
            # 2秒停止
            time.sleep(2)
            print()

            # STEP5. '5.アカリ'を(50,100)に背景リフレッシュなしで重ねて表示
            print("STEP5. display 5.アカリ at (50,100) without background refresh")
            # _textは'5.アカリ'
            _text = "5.アカリ"
            # _pos_xは50
            _pos_x = 50
            # _pos_yは40
            _pos_y = 100
            # 文字サイズは3
            _size = 3
            # 文字色は黒
            _text_color = Colors.BLACK
            # 背景色は紫
            _back_color = Colors.MAGENTA
            # _refreshをFalseにすることで前の背景表示を消さずに追記できる。
            _refresh = False
            # set_display_textを実行
            m5.set_display_text(
                _text, _pos_x, _pos_y, _size, _text_color, _back_color, _refresh
            )
            print("-> Set")
            # 2秒停止
            time.sleep(2)
            print()

            # STEP6. '6.アカリ'を(50,170)にリフレッシュなしで重ねて表示
            print("STEP6. display 6.アカリ at (50,170) without background refresh")
            # _textは'6.アカリ'
            _text = "6.アカリ"
            # _pos_xは50
            _pos_x = 50
            # _pos_yは170
            _pos_y = 170
            # 文字サイズは2
            _size = 2
            # 文字色はピンク
            _text_color = Colors.PINK
            # 背景色は灰
            _back_color = Colors.DARKGREY
            # _refreshをFalseにすることで前の表示を消さずに追記できる。
            _refresh = False
            # set_display_textを実行
            m5.set_display_text(
                _text, _pos_x, _pos_y, _size, _text_color, _back_color, _refresh
            )
            print("-> Set")
            # 2秒停止
            time.sleep(2)
            print()

            # STEP7. '7.灯'を中央に表示
            print("STEP7. display 7.灯 at middle center")
            # _textは'7.灯'
            _text = "7.灯"
            # 文字サイズは6
            _size = 6
            # 文字色は白
            _text_color = Colors.WHITE
            # 背景色は黒
            _back_color = Colors.BLACK
            # set_display_textを実行
            # pos_x,pos_yのみデフォルト引数を使用
            m5.set_display_text(
                _text, size=_size, text_color=_text_color, back_color=_back_color)
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
