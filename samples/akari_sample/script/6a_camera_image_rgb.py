#!/usr/bin/env python3
# coding:utf-8

"""
Camera image rgb sample
Created on 2022/04/16
@author: Kazuya Yamamoto
"""
import cv2
import depthai as dai


def main() -> None:
    """
    メイン関数
    """
    # OAK-Dのパイプライン作成
    pipeline = dai.Pipeline()

    # ソースとアウトプットの設定
    camRgb = pipeline.create(dai.node.ColorCamera)
    xoutVideo = pipeline.create(dai.node.XLinkOut)

    # ストリーミング名設定
    xoutVideo.setStreamName("video")

    # RGBのカメラ、1080P、解像度1920x1080を指定
    camRgb.setBoardSocket(dai.CameraBoardSocket.RGB)
    camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
    camRgb.setVideoSize(1920, 1080)

    # キューのブロッキングなし、キューサイズ１を指定
    xoutVideo.input.setBlocking(False)
    xoutVideo.input.setQueueSize(1)

    # ソースとアウトプットを接続
    camRgb.video.link(xoutVideo.input)

    # デバイスをパイプラインに接続
    with dai.Device(pipeline) as device:
        video = device.getOutputQueue(name="video", maxSize=1, blocking=False)  # type: ignore

        # 画像を取得しウィンドウに描画
        while True:
            videoIn = video.get()
            cv2.imshow("video", videoIn.getCvFrame())

            # qを押されたら終了
            if cv2.waitKey(1) == ord("q"):
                break


if __name__ == "__main__":
    main()
