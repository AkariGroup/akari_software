#!/bin/bash

SCRIPT_DIR=$(cd $(dirname ${BASH_SOURCE:-$0}); pwd)
REPOSITORY_ROOT=$(realpath ${SCRIPT_DIR}/../../)

export HOST_GID=$(id -g)
export HOST_UID=$(id -u)
export DOCKER_GID=$(getent group docker | cut -d: -f3)

export AKARI_REPOSITORY_DIR=${REPOSITORY_ROOT}
export AKIRA_DEV_PROJECT_DIR=${SCRIPT_DIR}/.projects
