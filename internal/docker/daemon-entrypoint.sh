#!/bin/sh

set -e

USER_ID=${HOST_UID:-9001}
GROUP_ID=${HOST_GID:-9001}
USERNAME=user
GROUPNAME=group

addgroup -g $GROUP_ID $GROUPNAME
adduser -u $USER_ID -G $GROUPNAME -h /home/$USERNAME -D $USERNAME

exec /usr/bin/gosu $USERNAME "$@"
