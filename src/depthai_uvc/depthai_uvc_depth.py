import cv2
import depthai as dai
import numpy as np
import pyvirtualcam

# Create pipeline
pipeline = dai.Pipeline()
camLeft = pipeline.create(dai.node.MonoCamera)
camRight = pipeline.create(dai.node.MonoCamera)
stereo = pipeline.create(dai.node.StereoDepth)
xout = pipeline.create(dai.node.XLinkOut)
xout.setStreamName("depth")
stereo.setDefaultProfilePreset(dai.node.StereoDepth.PresetMode.HIGH_DENSITY)
# Black, to better see the cutout# Better handling for occlusions:
stereo.setRectifyEdgeFillColor(0)
stereo.setLeftRightCheck(False)
# Closer-in minimum depth, disparity range is doubled:
stereo.setExtendedDisparity(False)
# Better accuracy for longer distance, fractional disparity 32-levels:
stereo.setSubpixel(False)
stereo.disparity.link(xout.input)

camLeft.out.link(stereo.left)
camRight.out.link(stereo.right)

# Connect to device and start pipeline
with dai.Device(pipeline) as device, pyvirtualcam.Camera(
    width=640, height=480, device="/dev/video20", fps=150
) as uvc:
    qDepth = device.getOutputQueue(name="depth", maxSize=4, blocking=False)  # type: ignore
    print("UVC running")
    while True:
        inDisparity = (
            qDepth.get()
        )  # blocking call, will wait until a new data has arrived
        frameDepth = inDisparity.getFrame()
        # Normalization for better visualization
        frameDepth = (
            frameDepth * (255 / stereo.initialConfig.getMaxDisparity())
        ).astype(np.uint8)
        frameDepth = cv2.applyColorMap(frameDepth, cv2.COLORMAP_JET)
        uvc.send(frameDepth)
        if cv2.waitKey(1) == ord("q"):
            break
