# AKARI用自動起動セットアップスクリプト

#!/bin/bash
# -*- coding: utf-8 -*-
## シェルオプション
set -e           # コマンド実行に失敗したらエラー
set -u           # 未定義の変数にアクセスしたらエラー
set -o pipefail  # パイプのコマンドが失敗したらエラー（bashのみ）

SCRIPT_DIR=$(cd $(dirname $0); pwd)
. $AKARI_PARENT_PATH/setup/script/lib/common.bash    # 共通の関数や定数をライブラリからロード

trap errorHandler ERR

titleEcho "Copy auto start script to opt"
sudo cp -f $AKARI_PARENT_PATH/src/akari_autostart/default/auto_start.sh /opt
successEcho "Auto start script copied"

titleEcho "Add AKARI_PARENT_PATH to auto start script"
sudo sed -i -e "6,/AKARI_PARENT_PATH/c AKARI_PARENT_PATH=$AKARI_PARENT_PATH" /opt/auto_start.sh
successEcho "AKARI_PARENT_PATH was added in /opt/auto_start.sh"

titleEcho "Link auto start service to systemd"
if find /etc/systemd/system/auto_start.service > /dev/null; then
 skipEcho "Auto start service has already been available."
else
 sudo ln -s $AKARI_PARENT_PATH/src/akari_autostart/default/auto_start.service /etc/systemd/system
 successEcho "Auto start service was added"
fi

titleEcho "Enable auto start daemon"
sudo systemctl enable auto_start.service
sudo systemctl start auto_start.service
successEcho "Auto start service was enabled"


finishEcho
