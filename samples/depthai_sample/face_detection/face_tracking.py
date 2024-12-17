#!/usr/bin/env python3

"""
Face detection sample
Created on 2022/04/16
Based on depthai-experiments
https://github.com/luxonis/depthai-experiments/tree/master/gen2-face-detection
"""

import argparse
import threading
import time
from pathlib import Path
from queue import Queue
from time import sleep
from typing import Any

import blobconverter
import cv2
import depthai as dai
import numpy as np
from akari_client import AkariClient
from utils.priorbox import PriorBox
from utils.utils import draw

pan_target_angle = 0.0
tilt_target_angle = 0.0

# resize input to smaller size for faster inference
NN_WIDTH, NN_HEIGHT = 160, 120
VIDEO_WIDTH, VIDEO_HEIGHT = 640, 480


# 顔追従するクラス
class FaceTracker:
    """face tracking class"""

    def __init__(self) -> None:
        global pan_target_angle
        global tilt_target_angle

        # AkariControllerのインスタンスを作成する
        self.akari = AkariClient()
        self.joints = self.akari.joints

        self._default_x = 0
        self._default_y = 0

        # サーボトルクON
        self.joints.enable_all_servo()
        # モータ速度設定
        self.joints.set_joint_velocities(pan=10, tilt=10)
        # モータ加速度設定
        self.joints.set_joint_accelerations(pan=30, tilt=30)

        # Initialize motor position
        self.joints.move_joint_positions(pan=0, tilt=0)
        while True:
            if (
                abs(self.joints.get_joint_positions()["pan"] - self._default_x) <= 0.087
                and abs(self.joints.get_joint_positions()["tilt"] - self._default_y)
                <= 0.087
            ):
                break
        self.currentMotorAngle = self.joints.get_joint_positions()

        # Dynamixel Input Value
        pan_target_angle = self.currentMotorAngle["pan"]
        tilt_target_angle = self.currentMotorAngle["tilt"]

    def _tracker(self) -> None:
        global pan_target_angle
        global tilt_target_angle
        while True:
            self.joints.move_joint_positions(
                pan=pan_target_angle, tilt=tilt_target_angle
            )
            sleep(0.01)


class DirectionUpdater:
    """Update direction from face info"""

    _H_PIX_WIDTH = VIDEO_WIDTH
    _H_PIX_HEIGHT = VIDEO_HEIGHT
    _PAN_THRESHOLD = 0.1
    _TILT_THRESHOLD = 0.1
    _pan_dev = 0
    _tilt_dev = 0
    # モータゲインの最大幅。追従性の最大はここで変更
    _MAX_PAN_GAIN = 0.1
    _MAX_TILT_GAIN = 0.1
    # モータゲインの最小幅。追従性の最小はここで変更
    _MIN_PAN_GAIN = 0.07
    _MIN_TILT_GAIN = 0.07
    # 顔の距離によってモータゲインを変化させる係数。上げると早い動きについていきやすいが、オーバーシュートしやすくなる。
    _GAIN_COEF_PAN = 0.0001
    _GAIN_COEF_TILT = 0.0001

    _pan_p_gain = _MIN_PAN_GAIN
    _tilt_p_gain = _MIN_TILT_GAIN

    _PAN_POS_MAX = 1.047
    _PAN_POS_MIN = -1.047
    _TILT_POS_MAX = 0.523
    _TILT_POS_MIN = -0.523

    def __init__(self) -> None:
        global prev_time
        global cur_time
        self._face_x = 0
        self._face_y = 0
        self._face_width = 0
        self._face_height = 0
        self._old_face_x: float = 0
        self._old_face_y: float = 0

    def _calc_p_gain(self) -> None:
        self._pan_p_gain = self._GAIN_COEF_PAN * self._face_width
        if self._pan_p_gain > self._MAX_PAN_GAIN:
            self._pan_p_gain = self._MAX_PAN_GAIN
        elif self._pan_p_gain < self._MIN_PAN_GAIN:
            self._pan_p_gain = self._MIN_PAN_GAIN
        self._tilt_p_gain = self._GAIN_COEF_TILT * self._face_width
        if self._tilt_p_gain > self._MAX_TILT_GAIN:
            self._tilt_p_gain = self._MAX_TILT_GAIN
        elif self._tilt_p_gain < self._MIN_TILT_GAIN:
            self._tilt_p_gain = self._MIN_TILT_GAIN

    def _face_info_cb(self, q_detection: Any) -> None:
        while True:
            self.detections = q_detection.get()

            self._face_x = self.detections[0]
            self._face_y = self.detections[1]

            self._face_width = self.detections[2]
            self._face_height = self.detections[3]

            self._set_goal_pos(
                self._face_x + self._face_width / 2,
                self._face_y + self._face_height / 2,
            )
            self._calc_p_gain()

    def _set_goal_pos(self, face_x: float, face_y: float) -> None:
        global pan_target_angle
        global tilt_target_angle
        if face_x >= 1000:
            face_x = 0
        if face_y >= 1000:
            face_y = 0
        pan_error = -(face_x + self._pan_dev - self._H_PIX_WIDTH / 2.0) / (
            self._H_PIX_WIDTH / 2.0
        )  # -1 ~ 1
        tilt_error = -(face_y + self._tilt_dev - self._H_PIX_HEIGHT / 2.0) / (
            self._H_PIX_HEIGHT / 2.0
        )  # -1 ~ 1

        if abs(pan_error) > self._PAN_THRESHOLD and not (face_x == self._old_face_x):
            pan_target_angle += self._pan_p_gain * pan_error
        if pan_target_angle < self._PAN_POS_MIN:
            pan_target_angle = self._PAN_POS_MIN
        elif pan_target_angle > self._PAN_POS_MAX:
            pan_target_angle = self._PAN_POS_MAX
        if abs(tilt_error) > self._TILT_THRESHOLD and not (face_y == self._old_face_y):
            tilt_target_angle += self._tilt_p_gain * tilt_error
        if tilt_target_angle < self._TILT_POS_MIN:
            tilt_target_angle = self._TILT_POS_MIN
        elif tilt_target_angle > self._TILT_POS_MAX:
            tilt_target_angle = self._TILT_POS_MAX

        self._old_face_x = face_x
        self._old_face_y = face_y


"""
YuNet face detection demo running on device with video input from host.
https://github.com/ShiqiYu/libfacedetection


Run as:
python3 -m pip install -r requirements.txt
python3 main.py

Blob is taken from:
https://github.com/PINTO0309/PINTO_model_zoo/tree/main/144_YuNet
"""


def FaceRecognition(q_detection: Any) -> None:
    # --------------- Arguments ---------------
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-nn",
        "--nn_model",
        help="Provide model name or model path for inference",
        default="face_detection_yunet_160x120",
        type=str,
    )
    parser.add_argument(
        "-conf",
        "--confidence_thresh",
        help="set the confidence threshold",
        default=0.6,
        type=float,
    )
    parser.add_argument(
        "-iou",
        "--iou_thresh",
        help="set the NMS IoU threshold",
        default=0.3,
        type=float,
    )
    parser.add_argument(
        "-topk",
        "--keep_top_k",
        default=750,
        type=int,
        help="set keep_top_k for results outputing.",
    )

    args = parser.parse_args()

    nn_path = args.nn_model
    if not Path(nn_path).exists():
        print("No blob found at {}. Looking into DepthAI model zoo.".format(nn_path))
        nn_path = str(
            blobconverter.from_zoo(
                args.nn_model, shaves=6, zoo_type="depthai", use_cache=True
            )
        )

    # --------------- Pipeline ---------------
    # Start defining a pipeline
    pipeline = dai.Pipeline()
    pipeline.setOpenVINOVersion(version=dai.OpenVINO.VERSION_2021_4)

    # Define a neural network that will detect faces
    detection_nn = pipeline.create(dai.node.NeuralNetwork)
    detection_nn.setBlobPath(nn_path)
    detection_nn.setNumPoolFrames(4)
    detection_nn.input.setBlocking(False)
    detection_nn.setNumInferenceThreads(2)

    # Define camera
    cam = pipeline.create(dai.node.ColorCamera)
    cam.setPreviewSize(VIDEO_WIDTH, VIDEO_HEIGHT)
    cam.setInterleaved(False)
    cam.setFps(40)
    cam.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)

    # Define manip
    manip = pipeline.create(dai.node.ImageManip)
    manip.initialConfig.setResize(NN_WIDTH, NN_HEIGHT)
    manip.initialConfig.setFrameType(dai.RawImgFrame.Type.BGR888p)
    manip.inputConfig.setWaitForMessage(False)

    # Create outputs
    xout_cam = pipeline.create(dai.node.XLinkOut)
    xout_cam.setStreamName("cam")

    xout_nn = pipeline.create(dai.node.XLinkOut)
    xout_nn.setStreamName("nn")

    cam.preview.link(manip.inputImage)
    cam.preview.link(xout_cam.input)
    manip.out.link(detection_nn.input)
    detection_nn.out.link(xout_nn.input)

    # --------------- Inference ---------------
    # Pipeline defined, now the device is assigned and pipeline is started
    with dai.Device(pipeline) as device:

        # Output queues will be used to get the rgb frames and nn data
        # from the outputs defined above
        q_cam = device.getOutputQueue("cam", 4, blocking=False)  # type: ignore
        q_nn = device.getOutputQueue(name="nn", maxSize=4, blocking=False)  # type: ignore

        start_time = time.time()
        counter = 0
        fps = 0.0

        while True:
            in_frame = q_cam.get()
            in_nn = q_nn.get()

            frame = in_frame.getCvFrame()

            # get all layers
            conf = np.array(in_nn.getLayerFp16("conf")).reshape((1076, 2))
            iou = np.array(in_nn.getLayerFp16("iou")).reshape((1076, 1))
            loc = np.array(in_nn.getLayerFp16("loc")).reshape((1076, 14))

            # decode
            pb = PriorBox(
                input_shape=(NN_WIDTH, NN_HEIGHT),
                output_shape=(frame.shape[1], frame.shape[0]),
            )
            dets = pb.decode(loc, conf, iou, args.confidence_thresh)

            # NMS
            if dets.shape[0] > 0:
                # NMS from OpenCV
                bboxes = dets[:, 0:4]
                scores = dets[:, -1]

                keep_idx = cv2.dnn.NMSBoxes(
                    bboxes=bboxes.tolist(),
                    scores=scores.tolist(),
                    score_threshold=args.confidence_thresh,
                    nms_threshold=args.iou_thresh,
                    eta=1,
                    top_k=args.keep_top_k,
                )  # returns [box_num, class_num]

                keep_idx = np.squeeze(keep_idx)  # type: ignore
                dets = dets[keep_idx]

            # Draw
            if dets.shape[0] > 0:

                if dets.ndim == 1:
                    dets = np.expand_dims(dets, 0)

                draw(
                    img=frame,
                    bboxes=dets[:, :4],
                    landmarks=np.reshape(dets[:, 4:14], (-1, 5, 2)),
                    scores=dets[:, -1],
                )

                # バウンディングボックスの値をQueueに挿入する
                q_detection.put(bboxes[0])

            # show fps
            color_black, color_white = (0, 0, 0), (255, 255, 255)
            label_fps = "Fps: {:.2f}".format(fps)
            (w1, h1), _ = cv2.getTextSize(label_fps, cv2.FONT_HERSHEY_TRIPLEX, 0.4, 1)
            cv2.rectangle(
                frame,
                (0, frame.shape[0] - h1 - 6),
                (w1 + 2, frame.shape[0]),
                color_white,
                -1,
            )
            cv2.putText(
                frame,
                label_fps,
                (2, frame.shape[0] - 4),
                cv2.FONT_HERSHEY_TRIPLEX,
                0.4,
                color_black,
            )

            # show frame
            cv2.imshow("Detections", frame)

            counter += 1
            if (time.time() - start_time) > 1:
                fps = counter / (time.time() - start_time)

                counter = 0
                start_time = time.time()

            if cv2.waitKey(1) == ord("q"):
                break


def main() -> None:
    q_detection: Any = Queue()

    face_tracker = FaceTracker()
    direction_updater = DirectionUpdater()

    t1 = threading.Thread(target=FaceRecognition, args=(q_detection,))
    t2 = threading.Thread(target=direction_updater._face_info_cb, args=(q_detection,))
    t3 = threading.Thread(target=face_tracker._tracker)
    t1.start()
    t2.start()
    t3.start()
    t1.join()
    t2.join()
    t3.join()


if __name__ == "__main__":
    main()
