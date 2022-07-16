# Akari sample py

## 概要
AKARIのサンプルアプリ集(非ROS版)

## 必要要件
AKARIを非ROS版に切り替えていること。  
切り替えていない場合は下記を実行する。  
`cd akarimainpc/setup/script`  
`./mainpc_setup_ros_disable_ver.sh`  

## 各サンプルの説明と実行方法
`script`ディレクトリ内部で実行する。
`cd script`

1a.モータ制御  
ヘッドのモータ制御サンプル。  
`python3 1a_motor_control.py`  

2a.ボタン入力  
ボタン入力のサンプル。ボタンを押すとコマンドラインにメッセージが出力される。  
`python3 2a_button.py`  

2b.GPIO入力  
GPIO入力のサンプル。コマンドラインにdin,ainの値が出力される。  
`python3 2b_gpio_input.py`  

2c.GPIO出力  
GPIO出力のサンプル。コマンドラインにdout,pwmoutの値が出力される。  
`python3 2c_gpio_output.py`  

2d.環境センサ  
環境センサのサンプル。コマンドラインに気圧、温度、明るさセンサの値が出力される。  
`python3 2d_env_info.py`  

2e.IMU  
IMUのサンプル。コマンドラインに加速度、ジャイロ、それらから算出された本体角度値が出力される。  
`python3 2e_imu_info.py`  

3a.GPIO出力制御  
GPIO出力制御のサンプル。ステップごとにdout,pwmoutの出力制御を行う。  
`python3 3a_gpio_control.py`  

4a.ディスプレイ背景カラー出力  
ディスプレイ背景カラー変更のサンプル。ステップごとにM5の背景カラー変更を行う。  
`python3 4a_display_color.py`  

4b.ディスプレイテキスト出力  
ディスプレイテキスト出力のサンプル。ステップごとにM5の画面にテキストを出力する。  
`python3 4b_display_text.py`  

4c.ディスプレイ画像出力  
ディスプレイ画像出力のサンプル。ステップごとにM5の画面に画像を出力する。  
`python3 4c_display_image.py`  

5a.IMU初期化  
IMU初期化のサンプル。一定時間ごとにIMU値を初期化する。  
`python3 5a_init_imu.py`  

5b.M5リセット  
M5リセットのサンプル。一定時間ごとにM5をリセットする。  
`python3 5b_reset_m5.py`  

6a.RGBカメラ表示  
RGBカメラ映像表示のサンプル。RGB画像をストリーミングする。  
`python3 6a_camera_image_rgb.py`  

6b.ステレオdepthカメラ表示  
ステレオdepthカメラ映像表示のサンプル。  
ステレオdepthによる距離画像をストリーミングする。  
`python3 6b_camera_image_stereo_depth.py`  
