#!/bin/bash
# -*- coding: utf-8 -*-
## シェルオプション
set -e           # コマンド実行に失敗したらエラー
set -u           # 未定義の変数にアクセスしたらエラー
set -o pipefail  # パイプのコマンドが失敗したらエラー（bashのみ）

(
cd internal/docker
. env.sh
export AKIRA_IMAGE_TAG=develop
#docker compose -f docker-compose.dev.yml build
gnome-terminal -- bash -c "docker compose -f docker-compose.dev.yml up"
)

(
cd internal/akira_frontend
npm run prebuild
npm run start
)
