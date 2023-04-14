#!/usr/bin/env python3

"""
Object detection sample(mobilenet SSD)
Created on 2022/04/16
Based on depthai-python
https://github.com/luxonis/depthai-python/tree/main/examples/MobileNet
"""

import argparse
import json
import time
from pathlib import Path
from typing import Any, List, Tuple

import cv2
import depthai as dai
import numpy as np
import blobconverter


configPathDefault = str(
    (Path(__file__).parent / Path("configs/mobilenet-ssd.json")).resolve().absolute()
)
parser = argparse.ArgumentParser()
parser.add_argument(
    "-n",
    "--nnPath",
    nargs="?",
    help="Provide model name or model path for mobilenet detection network",
    default="mobilenet-ssd",
    type=str
)
parser.add_argument(
    "-c",
    "--configPath",
    nargs="?",
    help="Path to mobilenet detection label",
    default=configPathDefault,
    type=str
)
parser.add_argument(
    "-s",
    "--sync",
    action="store_true",
    help="Sync RGB output with NN output",
    default=False,
)
args = parser.parse_args()

# get model path
nnPath = args.nnPath
if not Path(nnPath).exists():
    print("No blob found at {}. Looking into DepthAI model zoo.".format(nnPath))
    nnPath = str(blobconverter.from_zoo(args.nnPath, shaves = 6, use_cache=True))

json_open = open(str(args.configPath), "r")
config = json.load(json_open)
# MobilenetSSD label texts
labelMap = config["mappings"]["labels"]

# Create pipeline
pipeline = dai.Pipeline()

# Define sources and outputs
camRgb = pipeline.create(dai.node.ColorCamera)
nn = pipeline.create(dai.node.MobileNetDetectionNetwork)
xoutRgb = pipeline.create(dai.node.XLinkOut)
nnOut = pipeline.create(dai.node.XLinkOut)

xoutRgb.setStreamName("rgb")
nnOut.setStreamName("nn")
w, h = map(int, config["nn_config"]["input_size"].split("x"))
# Properties
camRgb.setPreviewSize(w, h)
camRgb.setInterleaved(False)
camRgb.setFps(40)
# Define a neural network that will make predictions based on the source frames
nn.setConfidenceThreshold(config["nn_config"]["confidence_threshold"])
nn.setBlobPath(nnPath)
nn.setNumInferenceThreads(2)
nn.input.setBlocking(False)

# Linking
if args.sync:
    nn.passthrough.link(xoutRgb.input)
else:
    camRgb.preview.link(xoutRgb.input)

camRgb.preview.link(nn.input)
nn.out.link(nnOut.input)

# Connect to device and start pipeline
with dai.Device(pipeline) as device:

    # Output queues will be used to get the rgb frames and nn data
    # from the outputs defined above
    qRgb = device.getOutputQueue(name="rgb", maxSize=4, blocking=False)  # type: ignore
    qDet = device.getOutputQueue(name="nn", maxSize=4, blocking=False)  # type: ignore

    frame = None
    detections: List[Any] = []
    startTime = time.monotonic()
    counter = 0
    color2 = (255, 255, 255)

    # nn data (bounding box locations) are in <0..1> range -
    # they need to be normalized with frame width/height
    def frameNorm(frame: Any, bbox: Tuple[Any, Any, Any, Any]) -> Any:
        normVals = np.full(len(bbox), frame.shape[0])
        normVals[::2] = frame.shape[1]
        return (np.clip(np.array(bbox), 0, 1) * normVals).astype(int)

    def displayFrame(name: str, frame: object) -> None:
        color = (255, 0, 0)
        for detection in detections:
            bbox = frameNorm(
                frame, (detection.xmin, detection.ymin, detection.xmax, detection.ymax)
            )
            cv2.putText(
                frame,
                labelMap[detection.label],
                (bbox[0] + 10, bbox[1] + 20),
                cv2.FONT_HERSHEY_TRIPLEX,
                0.5,
                color,
            )
            cv2.putText(
                frame,
                f"{int(detection.confidence * 100)}%",
                (bbox[0] + 10, bbox[1] + 40),
                cv2.FONT_HERSHEY_TRIPLEX,
                0.5,
                color,
            )
            cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), color, 2)
        # Show the frame
        cv2.imshow(name, cv2.resize(frame, (640, 640)))

    while True:
        if args.sync:
            # Use blocking get() call to catch frame and inference result synced
            inRgb = qRgb.get()
            inDet = qDet.get()
        else:
            # Instead of get (blocking), we use tryGet (nonblocking)
            # which will return the available data or None otherwise
            inRgb = qRgb.tryGet()
            inDet = qDet.tryGet()

        if inRgb is not None:
            frame = inRgb.getCvFrame()
            cv2.putText(
                frame,
                "NN fps: {:.2f}".format(counter / (time.monotonic() - startTime)),
                (2, frame.shape[0] - 4),
                cv2.FONT_HERSHEY_TRIPLEX,
                0.4,
                color2,
            )

        if inDet is not None:
            detections = inDet.detections
            counter += 1

        # If the frame is available, draw bounding boxes on it and show the frame
        if frame is not None:
            displayFrame("rgb", frame)

        if cv2.waitKey(1) == ord("q"):
            break
