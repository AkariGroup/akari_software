import uvicorn
from akira_controller_server.api import api
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(api)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def serve(host: str, port: int) -> None:
    uvicorn.run(
        f"{__name__}:app",
        host=host,
        port=port,
    )
