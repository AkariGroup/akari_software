#!/usr/bin/env python3

import argparse
import json
import time
from pathlib import Path
from typing import Any, List, Tuple, cast

import blobconverter
import cv2
import depthai as dai
import numpy as np

# Get argument first
configPathDefault = str(
    (Path(__file__).parent / Path("configs/yolov4tiny_coco_416x416.json")).resolve().absolute()
)
parser = argparse.ArgumentParser()
parser.add_argument(
    "-n",
    "--nnPath",
    nargs="?",
    help="Path to YOLO detection network blob",
    default="yolov4_tiny_coco_416x416",
)
parser.add_argument(
    "-c",
    "--configPath",
    nargs="?",
    help="Path to mobilenet detection label",
    default=configPathDefault,
)
args = parser.parse_args()

# get model path
nnPath = args.nnPath
if not Path(nnPath).exists():
    print("No blob found at {}. Looking into DepthAI model zoo.".format(nnPath))
    nnPath = str(
        blobconverter.from_zoo(
            args.nnPath, shaves=6, zoo_type="depthai", use_cache=True
        )
    )
if not Path(args.configPath).exists():
    raise ValueError("Path {} does not exist!".format(args.configPath))
with Path(args.configPath).open() as f:
    config = json.load(f)
nnConfig = config.get("nn_config", {})
width = 416
height = 416
# parse input shape
if "input_size" in nnConfig:
    width, height = tuple(map(int, nnConfig.get("input_size").split("x")))
# tiny yolo v4 label texts
labelMap = config["mappings"]["labels"]
metadata = nnConfig.get("NN_specific_metadata", {})

syncNN = True

# Create pipeline
pipeline = dai.Pipeline()

# Define sources and outputs
camRgb = pipeline.create(dai.node.ColorCamera)
detectionNetwork = cast(
    dai.node.YoloDetectionNetwork, pipeline.create(dai.node.YoloDetectionNetwork)
)
xoutRgb = pipeline.create(dai.node.XLinkOut)
nnOut = pipeline.create(dai.node.XLinkOut)

xoutRgb.setStreamName("rgb")
nnOut.setStreamName("nn")

# Properties
camRgb.setPreviewSize(width, height)
camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
camRgb.setInterleaved(False)
camRgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.BGR)
camRgb.setFps(40)

# Network specific settings
detectionNetwork.setConfidenceThreshold(metadata.get("confidence_threshold", {}))
detectionNetwork.setNumClasses(metadata.get("classes", {}))
detectionNetwork.setCoordinateSize(metadata.get("coordinates", {}))
detectionNetwork.setAnchors(metadata.get("anchors", {}))
detectionNetwork.setAnchorMasks(metadata.get("anchor_masks", {}))
detectionNetwork.setIouThreshold(metadata.get("iou_threshold", {}))
detectionNetwork.setBlobPath(nnPath)
detectionNetwork.setNumInferenceThreads(2)
detectionNetwork.input.setBlocking(False)

# Linking
camRgb.preview.link(detectionNetwork.input)
if syncNN:
    detectionNetwork.passthrough.link(xoutRgb.input)
else:
    camRgb.preview.link(xoutRgb.input)

detectionNetwork.out.link(nnOut.input)

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

    # nn data, being the bounding box locations, are in <0..1> range -
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
                255,
            )
            cv2.putText(
                frame,
                f"{int(detection.confidence * 100)}%",
                (bbox[0] + 10, bbox[1] + 40),
                cv2.FONT_HERSHEY_TRIPLEX,
                0.5,
                255,
            )
            cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), color, 2)
        # Show the frame
        cv2.imshow(name, frame)

    while True:
        if syncNN:
            inRgb = qRgb.get()
            inDet = qDet.get()
        else:
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

        if frame is not None:
            displayFrame("rgb", frame)

        if cv2.waitKey(1) == ord("q"):
            break
