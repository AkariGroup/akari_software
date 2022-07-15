# AKARI用ツールインストールスクリプト

#!/bin/bash
# -*- coding: utf-8 -*-
## シェルオプション
set -e           # コマンド実行に失敗したらエラー
set -u           # 未定義の変数にアクセスしたらエラー
set -o pipefail  # パイプのコマンドが失敗したらエラー（bashのみ）

SCRIPT_DIR=$(cd $(dirname $0); pwd)
. $AKARI_PARENT_PATH/setup/script/lib/common.bash    # 共通の関数や定数をライブラリからロード

titleEcho "Install vscode" #vscodeインストールするため、インストーラをcurlで取得する
if (dpkg -l | grep "vscode" > /dev/null); then
 skipEcho "vscode has available."
else
 curl -sL https://go.microsoft.com/fwlink/?LinkID=760868 -o vscode.deb | sudo -E bash -
 sudo apt -y install ./vscode.deb
 rm vscode.deb
 successEcho "vscode was installed."
fi

echo -e " "
echo -e "\e[32;1m----------------------------------------\e[m"
echo -e "\e[32;1mAll steps were finished!!\e[m"
echo -e "\e[32;1m----------------------------------------\e[m"
echo -e " "
