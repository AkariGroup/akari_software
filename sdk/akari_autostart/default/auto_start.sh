#!/bin/bash
#--------------------------------------------------------------------
#バックグラウンド実行用のスクリプト
#--------------------------------------------------------------------

# set upスクリプト内で/optにこのファイルをコピー後、akari_mainのパスを下行に設定する。
# AKARI_PARENT_PATH = ""

export PATH="$HOME/.poetry/bin:$PATH"
cd $AKARI_PARENT_PATH
poetry run python3 tools/python/servo_start.py
poetry run python3 tools/python/m5_init.py

