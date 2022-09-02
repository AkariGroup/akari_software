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

        # アプリが終了されるまでループする。
        while True:
            # STEP1. M5のSDカード内の画像'/logo320_ex.jpg'を表示
            print("STEP1. display /logo320_ex.jpg in SD")
            # filepathでM5のSDカード内の画像パスを指定
            filepath = "/logo320_ex.jpg"
            # pos_xは0-320で座標指定。0もしくはPositions.LEFTで左揃え
            pos_x = Positions.LEFT
            # pos_yは0-240で座標指定。0もしくはPositions.TOPで上揃え
            pos_y = Positions.TOP
            # scaleでサイズ指定。マイナス値を入れると画面サイズに合わせて自動調整される。
            scale = -1.0
            # set_display_imageを実行
            m5.set_display_image(filepath, pos_x, pos_y, scale)
            print("-> Set")
            # 2秒停止
            time.sleep(2)
            print()

            # STEP2. M5のSDカード内の画像'/logo320.jpg'を2倍、中央揃えで表示
            print("STEP2. display /logo320.jpg in SD at x2 size at middle center")
            # filepathでM5のSDカード内の画像パスを指定
            filepath = "/logo320.jpg"
            # pos_xは0-320で座標指定。Positions.CENTERで左右中央
            pos_x = Positions.CENTER
            # pos_yは0-240で座標指定。Positions.CENTERで上下中央
            pos_y = Positions.CENTER
            # scaleでサイズ指定。
            scale = 2.0
            # set_display_imageを実行
            m5.set_display_image(filepath, pos_x, pos_y, scale)
            print("-> Set")
            # 2秒停止
            time.sleep(2)
            print()

            # STEP3. M5のSDカード内の画像'/logo320.jpg'を0.3倍、右下揃えで表示
            print("STEP3. display /logo320.jpg in SD at x0.3 at bottom right")
            # filepathでM5のSDカード内の画像パスを指定
            filepath = "/logo320.jpg"
            # pos_xはPositions.RIGHTで右揃え
            pos_x = Positions.RIGHT
            # pos_yはPositions.BOTTOMで下揃え
            pos_y = Positions.BOTTOM
            # scaleでサイズ指定。
            scale = 0.3
            # set_display_imageを実行
            m5.set_display_image(filepath, pos_x, pos_y, scale)
            print("-> Set")
            # 2秒停止
            time.sleep(2)
            print()

            # STEP4. M5のSDカード内の画像'/logo320.jpg'を0.7倍、左中央揃えで表示
            print("STEP4. display /logo320.jpg in SD at x0.7 at middle left")
            # filepathでM5のSDカード内の画像パスを指定
            filepath = "/logo320.jpg"
            # pos_xは0-320で座標指定。0もしくはPositions.LEFTで左揃え
            pos_x = Positions.LEFT
            # pos_yは0-240で座標指定。Positions.CENTERで上下中央
            pos_y = Positions.CENTER
            # scaleでサイズ指定。
            scale = 0.7
            # set_display_imageを実行
            m5.set_display_image(filepath, pos_x, pos_y, scale)
            print("-> Set")
            # 2秒停止
            time.sleep(2)
            print()

            # STEP5. M5のSDカード内の画像'/logo320.jpg'を0.4倍、右上揃えで表示
            print("STEP5. display /logo320.jpg in SD at x0.4 at top right")
            # filepathでM5のSDカード内の画像パスを指定
            filepath = "/logo320.jpg"
            # pos_xはPositions.RIGHTで右揃え
            pos_x = Positions.RIGHT
            # pos_yは0もしくはPositions.TOPで上揃え
            pos_y = Positions.TOP
            # scaleでサイズ指定。
            scale = 0.4
            # set_display_imageを実行
            m5.set_display_image(filepath, pos_x, pos_y, scale)
            print("-> Set")
            # 2秒停止
            time.sleep(2)
            print()

            # STEP6. M5のSDカード内の画像'/logo320.jpg'を0.2倍、左下揃えで表示
            print("STEP6. display /logo320.jpg in SD at x0.2 at bottom left")
            # filepathでM5のSDカード内の画像パスを指定
            filepath = "/logo320.jpg"
            # pos_xは0もしくはPositions.LEFTで左揃え
            pos_x = Positions.LEFT
            # pos_yはPositions.BOTTOMで下揃え
            pos_y = Positions.BOTTOM
            # scaleでサイズ指定。
            scale = 0.2
            # set_display_imageを実行
            m5.set_display_image(filepath, pos_x, pos_y, scale)
            print("-> Set")
            # 2秒停止
            time.sleep(2)
            print()

            # STEP7. M5のSDカード内の画像'/logo320.jpg'を0.3倍で(50,20)に表示
            print("STEP7. display /logo320.jpg in SD at x0.3 size at (50,20)")
            # filepathでM5のSDカード内の画像パスを指定
            filepath = "/logo320.jpg"
            # pos_xは0-320で座標指定。
            pos_x = 50
            # pos_yは0-240で座標指定。
            pos_y = 20
            # scaleでサイズ指定。
            scale = 0.3
            # set_display_imageを実行
            m5.set_display_image(filepath, pos_x, pos_y, scale)
            print("-> Set")
            # 2秒停止
            time.sleep(2)
            print()

            # STEP8. M5のSDカード内の画像'/logo320.jpg'を表示
            print("STEP8. display /logo320.jpg in SD")
            # filepathでM5のSDカード内の画像パスを指定
            filepath = "/logo320.jpg"
            # pos_xは0もしくはPositions.LEFTで左揃え
            pos_x = Positions.LEFT
            # pos_yは0もしくはPositions.TOPで上揃え
            pos_y = Positions.TOP
            # scaleでサイズ指定。マイナス値で画面に合わせて自動調整。
            scale = -1.0
            # set_display_imageを実行
            m5.set_display_image(filepath, pos_x, pos_y, scale)
            print("-> Set")
            # 2秒停止
            time.sleep(2)
            print()

            print("Finish!")
            # 5秒停止
            time.sleep(5)
            print()


if __name__ == "__main__":
    main()
