#!/bin/sh

set -eux

USER_ID=${HOST_UID:-9001}
GROUP_ID=${HOST_GID:-9001}
DOCKER_GROUP_ID=${DOCKER_GID:-9002}

USERNAME=user

# Create entries
getent passwd $USERNAME || useradd -u $USER_ID $USERNAME
getent group $USERNAME || groupadd -g $GROUP_ID $USERNAME
getent group docker || groupadd -g $DOCKER_GROUP_ID docker

# Update group ids
groupmod -g $GROUP_ID $USERNAME
groupmod -g $DOCKER_GROUP_ID docker

# Set user entry
usermod -g $GROUP_ID -u $USER_ID -G $USERNAME,docker $USERNAME

exec /usr/bin/gosu $USERNAME "$@"
