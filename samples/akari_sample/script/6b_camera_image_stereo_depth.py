#!/usr/bin/env python3

"""
Camera image stereo depth sample
Created on 2022/04/16
@author: Kazuya Yamamoto
"""
import cv2
import depthai as dai
import numpy as np


def main() -> None:
    """
    メイン関数
    """
    # OAK-Dのパイプライン作成
    pipeline = dai.Pipeline()

    # ソースとアウトプットの設定
    camLeft = pipeline.create(dai.node.MonoCamera)
    camRight = pipeline.create(dai.node.MonoCamera)
    stereo = pipeline.create(dai.node.StereoDepth)
    xoutDepth = pipeline.create(dai.node.XLinkOut)

    # ストリーミング名設定
    xoutDepth.setStreamName("depth")

    # ソースとアウトプットを接続
    camLeft.out.link(stereo.left)
    camRight.out.link(stereo.right)
    stereo.disparity.link(xoutDepth.input)

    # デバイスをパイプラインに接続
    with dai.Device(pipeline) as device:
        video = device.getOutputQueue(name="depth", maxSize=4, blocking=False)  # type: ignore

        # 画像を取得しウィンドウに描画
        while True:
            frame = video.get().getCvFrame()
            # フレームをカラーマップに割り当て
            frame = (frame * (255 / stereo.initialConfig.getMaxDisparity())).astype(
                np.uint8
            )
            frame = cv2.applyColorMap(frame, cv2.COLORMAP_JET)
            cv2.imshow("video", frame)

            # qを押されたら終了
            if cv2.waitKey(1) == ord("q"):
                break


if __name__ == "__main__":
    main()
