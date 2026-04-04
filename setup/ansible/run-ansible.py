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


def ensure_uv() -> str:
    """uvがインストールされていなければ自動インストールし、パスを返す。"""
    uv_path = shutil.which("uv")
    if uv_path:
        return uv_path

    # ~/.local/bin/uv もチェック
    local_uv = pathlib.Path.home() / ".local" / "bin" / "uv"
    if local_uv.exists():
        return str(local_uv)

    print("uv が見つかりません。インストール中...")
    subprocess.check_call(
        ["bash", "-c", "curl -LsSf https://astral.sh/uv/install.sh | sh"]
    )

    if local_uv.exists():
        return str(local_uv)

    # インストール後に再度検索
    uv_path = shutil.which("uv")
    if uv_path:
        return uv_path

    print("uv のインストールに失敗しました。手動でインストールしてください。")
    print("  curl -LsSf https://astral.sh/uv/install.sh | sh")
    sys.exit(1)


def setup_venv(uv: str) -> None:
    if (VENV_DIR / "bin" / "activate").exists():
        return

    print("venv を作成中...")
    subprocess.check_call([uv, "venv", str(VENV_DIR)])


def install_dependencies(uv: str) -> None:
    requirements_path = BASE_DIR / "requirements.txt"
    assert requirements_path.exists()

    print("依存パッケージのインストール中...")
    subprocess.check_call(
        [
            uv,
            "pip",
            "install",
            "-r",
            str(requirements_path),
            "--python",
            str(VENV_DIR / "bin" / "python"),
        ]
    )


def command_on_venv(command: str) -> List[str]:
    activate_bin = VENV_DIR / "bin" / "activate"
    return ["bash", "-c", f"source {activate_bin}; {command}"]


def main() -> None:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--clean", action="store_true")
    args, remainder = parser.parse_known_args()

    if args.clean:
        shutil.rmtree(VENV_DIR, ignore_errors=True)

    uv = ensure_uv()
    setup_venv(uv)
    install_dependencies(uv)

    opts = " ".join(remainder)
    # playbookが指定されていない場合、デフォルトでsystem.ymlを使用
    if not remainder or all(r.startswith("-") for r in remainder):
        playbook = str(BASE_DIR / "system.yml")
        cmd = command_on_venv(f"ansible-playbook {opts} {playbook}")
    else:
        cmd = command_on_venv(f"ansible-playbook {opts}")
    os.execvp(cmd[0], cmd)


if __name__ == "__main__":
    main()
