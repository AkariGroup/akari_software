#!/bin/sh

export HOME=/host_var

# Create directory for local binaries
mkdir -p $HOME/.local/bin
export PATH=$HOME/.local/bin:$PATH

exec "$@"
