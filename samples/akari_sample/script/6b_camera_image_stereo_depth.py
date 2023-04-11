#!/usr/bin/env python3

"""
Camera image stereo depth sample
Created on 2022/04/16
@author: Kazuya Yamamoto
"""

import cv2
import depthai as dai
import numpy

MAX_DEPTH = 1500.0  # unit: [mm]


def main() -> None:
    """
    メイン関数
    """
    # OAK-Dのパイプライン作成
    pipeline = dai.Pipeline()

    # ソースとアウトプットの設定
    cam_left = pipeline.create(dai.node.MonoCamera)
    cam_left.setResolution(dai.MonoCameraProperties.SensorResolution.THE_480_P)
    cam_right = pipeline.create(dai.node.MonoCamera)
    cam_right.setResolution(dai.MonoCameraProperties.SensorResolution.THE_480_P)
    stereo = pipeline.create(dai.node.StereoDepth)
    xout_depth = pipeline.create(dai.node.XLinkOut)

    # ストリーミング名設定
    xout_depth.setStreamName("depth")

    # ソースとアウトプットを接続
    cam_left.out.link(stereo.left)
    cam_right.out.link(stereo.right)
    stereo.depth.link(xout_depth.input)

    # デバイスをパイプラインに接続
    with dai.Device(pipeline) as device:
        video = device.getOutputQueue(name="depth", maxSize=4, blocking=False)  # type: ignore

        # 画像を取得しウィンドウに描画
        while True:
            depth = video.get().getCvFrame()
            # フレームをカラーマップに割り当て
            depth[numpy.where(depth > MAX_DEPTH)] = 0
            norm_depth = (depth * (255 / MAX_DEPTH)).astype(numpy.uint8)
            colored_depth: numpy.ndarray = cv2.applyColorMap(
                norm_depth, cv2.COLORMAP_JET
            )
            cv2.imshow("video", colored_depth)

            # qを押されたら終了
            if cv2.waitKey(1) == ord("q"):
                break


if __name__ == "__main__":
    main()
