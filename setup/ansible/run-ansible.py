#!/usr/bin/env python3

import argparse
import os
import pathlib
import shutil
import subprocess
import sys
from typing import List

BASE_DIR = pathlib.Path(__file__).resolve().parent
VENV_DIR = BASE_DIR / ".venv"
ACTIVATE_BIN = VENV_DIR / "bin/activate"


def command_on_venv(command: str) -> List[str]:
    return ["bash", "-c", f"source {str(ACTIVATE_BIN)}; {command}"]


def setup_venv() -> None:
    if ACTIVATE_BIN.exists():
        return

    try:
        import venv  # NOQA
    except ImportError:
        print(
            """venvがインストールされていません。以下のコマンドを実行して venv をインストールしてください。

sudo apt install python3-venv
"""
        )
        sys.exit(1)

    print("venv を作成中...")
    subprocess.check_call([sys.executable, "-m", "venv", str(VENV_DIR)])


def install_dependencies() -> None:
    requirements_path = BASE_DIR / "requirements.txt"
    assert requirements_path.exists()

    print("依存パッケージのインストール中...")
    subprocess.check_call(command_on_venv(f"pip install -r {requirements_path}"))


def main() -> None:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--clean")
    args, remainder = parser.parse_known_args()

    if args.clean:
        shutil.rmtree(VENV_DIR, ignore_errors=True)

    setup_venv()
    install_dependencies()

    opts = " ".join(remainder)
    cmd = command_on_venv(f"ansible-playbook {opts}")
    os.execvp(cmd[0], cmd)


if __name__ == "__main__":
    main()
