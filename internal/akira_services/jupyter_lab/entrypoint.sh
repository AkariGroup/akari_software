#!/bin/sh

export HOME=/host_var

# Create directory for local binaries
mkdir -p $HOME/.local/bin
export PATH=$HOME/.local/bin:$PATH

# Copy custom jupyter_lab_config to inject config
mkdir -p $HOME/.jupyter
cp /resources/jupyter_lab_config.py $HOME/.jupyter/

# Create venv if it doesn't exists
export VENV_BASE=$HOME/.venv
if [ ! -d "$VENV_BASE" ]
then
  echo "Initializing venv"
  python3 -m venv $VENV_BASE --system-site-packages
  . $VENV_BASE/bin/activate
  # In order to allow custom jupyterlab installation,
  # run `pip install` only once for a env
  pip install --no-index --find-links /wheel jupyterlab
else
  . $VENV_BASE/bin/activate
fi

exec "$@"
