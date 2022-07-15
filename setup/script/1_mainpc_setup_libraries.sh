#AKARIに必要なライブラリのインストール用スクリプト

#!/bin/bash
# -*- coding: utf-8 -*-
## シェルオプション
set -e           # コマンド実行に失敗したらエラー
set -u           # 未定義の変数にアクセスしたらエラー
set -o pipefail  # パイプのコマンドが失敗したらエラー（bashのみ）

SCRIPT_DIR=$(cd $(dirname $0); pwd)
AKARI_PARENT_PATH=$(cd $(dirname $(dirname $SCRIPT_DIR)); pwd)
. $AKARI_PARENT_PATH/setup/script/lib/common.bash    # 共通の関数や定数をライブラリからロード

trap errorHandler ERR

titleEcho "Add AKARI_PARENT_PATH in .bashrc"
if grep "AKARI_PARENT_PATH" ~/.bashrc > /dev/null; then
 skipEcho "Source to setup terminal script has already been available in .bashrc."
else
 echo "export AKARI_PARENT_PATH=$AKARI_PARENT_PATH" >> ~/.bashrc
 export AKARI_PARENT_PATH=$AKARI_PARENT_PATH
 successEcho "Source to setup terminal script is added in .bashrc."
fi

titleEcho "Install git"
apt_check_and_install git

titleEcho " Install ssh"
apt_check_and_install ssh

titleEcho " Install curl"
apt_check_and_install curl

titleEcho "Install python3-pip" 
apt_check_and_install python3-pip

titleEcho "Install python-is-python3"
apt_check_and_install python-is-python3

titleEcho " Install libudev"
apt_check_and_install libudev-dev

titleEcho " Install v4l2loopback-dkms"
apt_check_and_install v4l2loopback-dkms

titleEcho " Install poetry"
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
successEcho "poetry installed"

titleEcho "Add poetry path in .bashrc"
if grep 'export PATH="\$HOME/.poetry/bin:\$PATH"' ~/.bashrc > /dev/null; then 
 skipEcho "poetry path has already been available in .bashrc."
else
 echo 'export PATH="$HOME/.poetry/bin:$PATH"' >> ~/.bashrc
 successEcho "poetry path was added in .bashrc"
fi

titleEcho " Add current user to dialout group"
if groups $USER | grep dialout > /dev/null; then
 skipEcho "Current user has already been in dialout group"
else
 sudo adduser $USER dialout
 sudo usermod -a -G dialout $(whoami)
 successEcho "User was added to dialout."
fi

titleEcho "Install pipenv"
pip3_check_and_install pipenv

titleEcho "Install pyserial"
pip3_check_and_install pyserial

titleEcho "set up akari poetry env"
(
    source $HOME/.poetry/env
    cd $AKARI_PARENT_PATH
    poetry install
)


finishEcho

bash
