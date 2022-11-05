import uvicorn
from akira_controller_server.api import api
from fastapi import FastAPI

app = FastAPI()
app.include_router(api)


def serve(host: str, port: int) -> None:
    uvicorn.run(
        f"{__name__}:app",
        host=host,
        port=port,
    )
