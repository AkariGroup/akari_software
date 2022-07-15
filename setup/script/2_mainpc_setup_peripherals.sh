# AKARI用ペリフェラル環境インストールスクリプト

#!/bin/bash
# -*- coding: utf-8 -*-
## シェルオプション
set -e           # コマンド実行に失敗したらエラー
set -u           # 未定義の変数にアクセスしたらエラー
set -o pipefail  # パイプのコマンドが失敗したらエラー（bashのみ）

SCRIPT_DIR=$(cd $(dirname $0); pwd)
. $AKARI_PARENT_PATH/setup/script/lib/common.bash    # 共通の関数や定数をライブラリからロード

trap errorHandler ERR

titleEcho "Add dummy camera setting for OAK-D in .bashrc"
if find /etc/modules-load.d/v4l2loopback.conf > /dev/null 2>&1; then
 skipEcho "Dummy camera setting has already been available in .bashrc."
else
 echo "v4l2loopback" | sudo tee /etc/modules-load.d/v4l2loopback.conf
 echo "options v4l2loopback video_nr=20 card_label=\"OAK-D Video Source\" exclusive_caps=1" | sudo tee /etc/modprobe.d/v4l2loopback.conf
 sudo modprobe v4l2loopback
 successEcho "Dummy camera setting  was added in .bashrc"
fi

titleEcho "Add movidius usb rules"
if find /etc/udev/rules.d/80-movidius.rules > /dev/null 2>&1; then
 skipEcho "Movidius usb rules has already been available."
else
 echo 'SUBSYSTEM=="usb", ATTRS{idVendor}=="03e7", MODE="0666"' | sudo tee /etc/udev/rules.d/80-movidius.rules
 sudo udevadm control --reload-rules && sudo udevadm trigger
 successEcho "Movidius usb rules  was added"
fi

titleEcho "Download arduino IDE"
if find /usr/local/bin/arduino > /dev/null 2>&1; then
 skipEcho "arduino IDE has already been installed."
else
 (
  cd ~/
  wget https://downloads.arduino.cc/arduino-1.8.19-linux64.tar.xz
  tar Jxfv arduino-1.8.19-linux64.tar.xz
  rm arduino-1.8.19-linux64.tar.xz
  sudo ./arduino-1.8.19/install.sh
  successEcho "arduino IDE was installed."
 )
fi

titleEcho "Set up arduino environment"
if find /etc/udev/rules.d/99-arduino-101.rules > /dev/null 2>&1; then
 skipEcho "arduino set up has already done."
else
 (
  cd ~
  ./arduino-1.8.19/arduino-linux-setup.sh ${USER}
  successEcho "arduino environment setup finished."
 )
fi

titleEcho "link arduino libraries"
if find ~/Arduino/libraries > /dev/null 2>&1; then
 :
else
 mkdir -p ~/Arduino
 mkdir -p ~/Arduino/libraries
 (
  cd $AKARI_PARENT_PATH
  git submodule init
  git submodule update --recursive
 )
fi
# 一度シンボリックリンクがあった場合全部削除してからリンクを貼り直す
find ~/Arduino/libraries -type l | xargs rm -f
ln -sf $AKARI_PARENT_PATH/setup/arduino/libraries/* ~/Arduino/libraries/
successEcho "Arduino libraries were linked."

titleEcho "Add M5Stack rules"
if find /etc/udev/rules.d/99-m5stack.rules > /dev/null 2>&1; then
 skipEcho "M5Stack rules has already been available."
else
 echo 'KERNEL=="ttyUSB*",  ATTRS{idVendor}=="10c4", ATTRS{idProduct}=="ea60", ATTRS{product}=="CP2104 USB to UART Bridge Controller" SYMLINK+="ttyUSB_M5Stack"' | sudo tee --append /etc/udev/rules.d/99-m5stack.rules
 echo 'KERNEL=="ttyACM[0-9]*", SUBSYSTEM=="tty", ACTION=="add", ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="55d4", SYMLINK+="ttyUSB_M5Stack"' | sudo tee --append /etc/udev/rules.d/99-m5stack.rules
  sudo udevadm control --reload-rules
  sudo udevadm trigger
  successEcho "M5Stack rules was added."
fi

#TODO(Yamamoto): Check on new environment.
#初回のみakarimainpcフォルダから.arduino15をコピーしたい
#コピーされたものか確認するため、.arduino15フォルダ内に"copied_from_akarimainpc"というファイルを作成し、
#その有無で確認する。
titleEcho "Copy arduino settings folder"
if find ~/.arduino15/copied_from_akarimainpc > /dev/null 2>&1; then
 skipEcho "arduino setting folder has been copied."
else
 cp -rf $AKARI_PARENT_PATH/setup/arduino/.arduino15 ~/
 successEcho "Arduino settings folder was copied."
fi

titleEcho "Add dynamixel usb rules"
if find /etc/udev/rules.d/99-dynamixel.rules > /dev/null 2>&1; then
 skipEcho "Dynamixel usb rules has already been available."
else
 (
  cd $SCRIPT_DIR
  echo 'KERNEL=="ttyUSB*", DRIVERS=="ftdi_sio", MODE="0666", ATTR{device/latency_timer}="1", SYMLINK+="ttyUSB_dynamixel"' | sudo tee --append /etc/udev/rules.d/99-dynamixel.rules
  sudo udevadm control --reload-rules
  sudo udevadm trigger
successEcho "Dynamixel usb rules was added."
 )
fi

titleEcho "Change authentification of dynamixel to current user"
if ls -l /dev/ttyUSB0 | grep ${USER} > /dev/null; then
 skipEcho "Current user has already have dynamixel USB serial device authentification."
else
 sudo chown ${USER} /dev/ttyUSB0
 successEcho "Authentification of dynamixel USB serial device was changed to current user."
fi


finishEcho
