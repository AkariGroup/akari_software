# akari_autostart
akariの自動起動サービス

## ディレクトリ構成
ros2: 標準の自動起動サービス。カメラの露出補正オフ、モータの初期位置移動、ros2のm5serial serverの起動、ros2のカメラパブリッシャの起動を行う。  
default: 非ROS2版の自動起動サービス。カメラの露出補正オフ、モータの初期位置移動、m5serialのリセットが実行される。  
script: 上記の実行に必要なスクリプト。  

## セットアップ方法
### ROS2を使う場合
1. 下記のセットアップスクリプトを実行。(標準でセットアップされている。)  
`cd akarimainpc/setup/script`  
`./6_mainpc_setup_autostart.sh`  

### 非ROS環境で使う場合
1. 下記のセットアップスクリプトを実行。  
`cd akarimainpc/setup/script`  
`./mainpc_setup_ros_disable_ver.sh`  