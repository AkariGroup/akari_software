#!/bin/bash

export HOST_GID=$(id -g)
export HOST_UID=$(id -u)
export DOCKER_GID=$(getent group docker | cut -d: -f3)
export AKIRA_DOCKER_CREDENTIAL=$(cat ~/.config/akira/.akira_docker_credential)
export AKIRA_IMAGE_TAG=${AKIRA_IMAGE_TAG:-v1}

exec "$@"
