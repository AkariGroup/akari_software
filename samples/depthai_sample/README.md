# Depthai sample

## 概要
depthaiによるサンプルアプリ集

### 顔検出  
顔検出のサンプル。  
`cd face_detection`
`python3 face_detection.py`  

### 物体検出(mobilenet)  
mobilenetによる物体検出のサンプル。  
`cd object_recognition`
`python3 mobilenet.py`  

### 物体検出(yolo)  
yoloによる物体検出のサンプル。  
`cd object_recognition`  
(yolo v3の場合)`python3 tiny_yolo.py`  
(yolo v4の場合)`python3 tiny_yolo.py -n models/yolo-v4-tiny-tf_openvino_2021.4_6shave.blob`  