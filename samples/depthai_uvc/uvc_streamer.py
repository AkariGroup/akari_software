import cv2

DEVICE_INDEX = 20

cap = cv2.VideoCapture(DEVICE_INDEX)

if not cap.isOpened():
    print(
        "カメラを開けませんでした。\n"
        f"/dev/video{DEVICE_INDEX} が見つからないか、まだ映像が配信されていません。\n"
        "先に `uv run depthai_uvc_rgb.py` または `uv run depthai_uvc_depth.py` を起動して、\n"
        "仮想カメラ `/dev/video20` を立ち上げてください。"
    )
    raise SystemExit(1)

while True:
    ret, frame = cap.read()
    if not ret or frame is None or frame.size == 0:
        print(
            "映像フレームを取得できませんでした。\n"
            "仮想カメラ `/dev/video20` への配信が止まっている可能性があります。\n"
            "`uv run depthai_uvc_rgb.py` または `uv run depthai_uvc_depth.py` が"
            "起動したままか確認してください。"
        )
        break
    cv2.imshow("camera", frame)
    if cv2.waitKey(10) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
