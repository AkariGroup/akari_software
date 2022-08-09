#!/bin/bash

export AKIRA_IMAGE_TAG=${AKIRA_IMAGE_TAG:-develop}

SCRIPT_DIR=$(cd $(dirname ${BASH_SOURCE:-$0}); pwd)
REPOSITORY_ROOT=$(realpath ${SCRIPT_DIR}/../../)

export HOST_GID=$(id -g)
export HOST_UID=$(id -u)
export DOCKER_GID=$(getent group docker | cut -d: -f3)

export AKARI_REPOSITORY_DIR=${REPOSITORY_ROOT}
export AKIRA_DEV_LOCAL_DIR=${SCRIPT_DIR}/.local
export AKIRA_DOCKER_CREDENTIAL=$(cat .docker_credential)

# for local development
export AKIRA_TEMPLATE_DIR=${AKARI_REPOSITORY_DIR}/internal/akira_templates
export AKIRA_PROJECT_DIR=${AKIRA_DEV_LOCAL_DIR}/home/akari/projects
export AKIRA_ETC_DIR=${AKIRA_DEV_LOCAL_DIR}/etc/akira
export AKIRA_VAR_DIR=${AKIRA_DEV_LOCAL_DIR}/var/lib/akira
