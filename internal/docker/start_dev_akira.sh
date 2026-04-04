#!/bin/bash
# -*- coding: utf-8 -*-
## シェルオプション
set -e           # コマンド実行に失敗したらエラー
set -u           # 未定義の変数にアクセスしたらエラー
set -o pipefail  # パイプのコマンドが失敗したらエラー（bashのみ）

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE:-$0}")"; pwd)
REPOSITORY_ROOT=$(realpath "${SCRIPT_DIR}/../../")

. "${SCRIPT_DIR}/env.sh"
export AKIRA_IMAGE_TAG=develop

gnome-terminal -- bash -c "docker compose -f ${SCRIPT_DIR}/docker-compose.dev.yml up"

(
cd "${REPOSITORY_ROOT}/internal/akira_frontend"
if [ ! -d "node_modules" ]; then
  echo "node_modules not found. Running npm install..."
  npm install
fi
npm run prebuild
npm run start
)
