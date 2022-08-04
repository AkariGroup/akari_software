#!/bin/sh

set -eux

USER_ID=${HOST_UID:-9001}
GROUP_ID=${HOST_GID:-9001}
DOCKER_GROUP_ID=${DOCKER_GID:-9002}

USERNAME=user

get_entry() {
  ENTRY=$(getent $1 $2 | cut -d':' -f1)
  echo "$ENTRY"
}

remove_group_if_exists() {
  ENTRY=$(get_entry group $1)
  if [ ! -z "${ENTRY}" ]; then
    echo "Group: $ENTRY exists!"
    groupdel -f $ENTRY
  fi
}

remove_user_if_exists() {
  ENTRY=$(get_entry passwd $1)
  if [ ! -z "${ENTRY}" ]; then
    echo "User: $ENTRY exists!"
    userdel -f $ENTRY
  fi
}

# Remove existing entries
echo $(remove_user_if_exists $USER_ID)
echo $(remove_group_if_exists $GROUP_ID)
echo $(remove_group_if_exists $DOCKER_GROUP_ID)

# Create entries
getent passwd $USERNAME || useradd -u $USER_ID $USERNAME
getent group $USERNAME || groupadd -g $GROUP_ID $USERNAME
getent group docker || groupadd -g $DOCKER_GROUP_ID docker

# Update group ids
groupmod -g $GROUP_ID $USERNAME
groupmod -g $DOCKER_GROUP_ID docker

# Update user entry
usermod -g $GROUP_ID -u $USER_ID -G $USERNAME,docker $USERNAME

exec /usr/bin/gosu $USERNAME "$@"
