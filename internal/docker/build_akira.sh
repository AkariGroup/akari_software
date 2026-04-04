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

docker compose -f "${REPOSITORY_ROOT}/internal/akira_services/docker-compose.image.yml" build
docker compose -f "${SCRIPT_DIR}/docker-compose.dev.yml" build
