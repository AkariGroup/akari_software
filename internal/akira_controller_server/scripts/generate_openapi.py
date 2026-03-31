#!/usr/bin/env python3

import json
import pathlib

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from akira_controller_server.api import api

PACKAGE_DIR = pathlib.Path(__file__).resolve().parents[1]
OPENAPI_DIR = PACKAGE_DIR / "openapi"
OPENAPI_FILE = OPENAPI_DIR / "openapi.json"

_app = FastAPI()
_app.include_router(api)


def generate() -> None:
    openapi_content = get_openapi(
        title="AkiraControllerServer",
        version=_app.version,
        openapi_version=_app.openapi_version,
        description=_app.description,
        routes=api.routes,
    )
    OPENAPI_DIR.mkdir(parents=True, exist_ok=True)
    with OPENAPI_FILE.open("w") as f:
        json.dump(openapi_content, f)


if __name__ == "__main__":
    generate()
