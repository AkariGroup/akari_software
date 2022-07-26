#!/bin/sh

export HOME=/tmp/user

# Create directory for local binaries
mkdir -p $HOME/.local/bin
export PATH=$HOME/.local/bin:$PATH

# Copy custom jupyter_lab_config to inject config
mkdir -p $HOME/.jupyter
cp /resources/jupyter_lab_config.py $HOME/.jupyter/

exec "$@"
