import os
import depthai as dai
import pyvirtualcam

# Reset v4l2loopback
os.system("sudo modprobe -r v4l2loopback")
os.system("sudo modprobe v4l2loopback")

# Create pipeline
pipeline = dai.Pipeline()
cam = pipeline.create(dai.node.ColorCamera)
cam.setColorOrder(dai.ColorCameraProperties.ColorOrder.RGB)
cam.setPreviewSize(1920, 1080)
xout = pipeline.create(dai.node.XLinkOut)
xout.setStreamName("rgb")
cam.preview.link(xout.input)
# Connect to device and start pipeline
with dai.Device(pipeline) as device, pyvirtualcam.Camera(
    width=1920, height=1080, device="/dev/video20", fps=30
) as uvc:
    qRgb = device.getOutputQueue(name="rgb", maxSize=4, blocking=False)  # type: ignore
    print("UVC running")
    while True:
        frame = qRgb.get().getFrame()
        uvc.send(frame)
