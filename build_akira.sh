#!/bin/bash
# -*- coding: utf-8 -*-
## シェルオプション
set -e           # コマンド実行に失敗したらエラー
set -u           # 未定義の変数にアクセスしたらエラー
set -o pipefail  # パイプのコマンドが失敗したらエラー（bashのみ）

(
cd internal
. docker/env.sh
export AKIRA_IMAGE_TAG=develop
docker compose -f akira_services/docker-compose.image.yml build
docker compose -f docker/docker-compose.dev.yml build
)
