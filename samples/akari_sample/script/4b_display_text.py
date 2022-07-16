#!/usr/bin/env python
# coding:utf-8

"""
Display text sample
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
        # STEP1. '1.AKARI'を左上表示
        print("STEP1. display 1.AKARI at top left")
        # textは'1.AKARI'
        text = "1.AKARI"
        # pos_xは0-320で座標指定。0が左
        pos_x = 0
        # pos_yは0-240で座標指定。0が上
        pos_y = 0
        # 文字サイズは3
        size = 3
        # 文字色は黒
        text_color = "black"
        # 背景色は白
        back_color = "white"
        # 背景全体をリセット
        refresh = True
        # set_display_textを実行
        result = m5.set_display_text(
            text, pos_x, pos_y, size, text_color, back_color, refresh
        )
        # 結果を出力
        print("Result: " + str(result))
        # 2秒停止
        time.sleep(2)
        print()

        # STEP2. '2.あかり'を中央に表示
        print("STEP2. display 2.あかり at middle center")
        text = "2.あかり"
        # pos_xは-999で左右中央
        pos_x = -999
        # pos_yは-999で上下中央
        pos_y = -999
        # 文字サイズは3
        size = 3
        # 文字色は赤
        text_color = "red"
        # 背景色は白
        back_color = "white"
        # 背景全体をリセット
        refresh = True
        # set_display_textを実行
        result = m5.set_display_text(
            text, pos_x, pos_y, size, text_color, back_color, refresh
        )
        # 結果を出力
        print("Result: " + str(result))
        # 2秒停止
        time.sleep(2)
        print()

        # STEP3. '3.灯り'を右下揃えに表示
        print("STEP3. display 3.灯り at bottom right")
        # textは'3.灯り'
        text = "3.灯り"
        # pos_xは999で右揃え
        pos_x = 999
        # pos_yは999で下揃え
        pos_y = 999
        # 文字サイズは4
        size = 4
        # 文字色は白
        text_color = "white"
        # 背景色は緑
        back_color = "green"
        # 背景全体をリセット
        refresh = True
        # set_display_textを実行
        result = m5.set_display_text(
            text, pos_x, pos_y, size, text_color, back_color, refresh
        )
        # 結果を出力
        print("Result: " + str(result))
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
        text_color = "blue"
        # 背景色は黄
        back_color = "yellow"
        # 背景全体をリセット
        refresh = True
        # set_display_textを実行
        result = m5.set_display_text(
            text, pos_x, pos_y, size, text_color, back_color, refresh
        )
        # 結果を出力
        print("Result: " + str(result))
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
        text_color = "black"
        # 背景色は紫
        back_color = "magenta"
        # refreshをFalseにすることで前の背景表示を消さずに追記できる。
        refresh = False
        # set_display_textを実行
        result = m5.set_display_text(
            text, pos_x, pos_y, size, text_color, back_color, refresh
        )
        # 結果を出力
        print("Result: " + str(result))
        # 2秒停止
        time.sleep(2)
        print()

        # STEP.6 フォントを軽量内蔵フォントに変更する。
        print("STEP6. Change font")
        # dataをFalseにすることで、フォントを内蔵フォントに変更可能
        data = False
        result = m5.use_japanese_font(data)
        # 結果を出力
        print("Result: " + str(result))
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
        text_color = "pink"
        # 背景色は灰
        back_color = "darkgrey"
        # refreshをFalseにすることで前の表示を消さずに追記できる。
        refresh = False
        # set_display_textを実行
        result = m5.set_display_text(
            text, pos_x, pos_y, size, text_color, back_color, refresh
        )
        # 結果を出力
        print("Result: " + str(result))
        # 2秒停止
        time.sleep(2)
        print()

        # STEP.8 フォントをデフォルトフォントに変更する。
        print("STEP8. Change font to default")
        # dataをTrueにすることで、フォントをデフォルトフォントに変更可能
        data = True
        result = m5.use_japanese_font(data)
        # 結果を出力
        print("Result: " + str(result))
        # 2秒停止
        time.sleep(2)
        print()

        # STEP9. '9.灯'を中央に表示
        print("STEP9. display 9.灯 at middle center")
        # textは'9.灯'
        text = "9.灯"
        # pos_xは-999で左右中央
        pos_x = -999
        # pos_yは-999で上下中央
        pos_y = -999
        # 文字サイズは6
        size = 6
        # 文字色は白
        text_color = "white"
        # 背景色は黒
        back_color = "black"
        # 背景全体をリセット
        refresh = True
        # set_display_textを実行
        result = m5.set_display_text(
            text, pos_x, pos_y, size, text_color, back_color, refresh
        )
        # 結果を出力
        print("Result: " + str(result))
        # 2秒停止
        time.sleep(2)
        print()

        print("Finish!")
        print()
        # 5秒停止
        time.sleep(5)


if __name__ == "__main__":
    main()
