from akira_controller_server.media import CaptureMode
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from ._context import get_context

router = APIRouter()


@router.get("/stream")
async def get_stream() -> StreamingResponse:
    context = get_context()
    return StreamingResponse(
        context.media_controller.consumer(),
        media_type="multipart/x-mixed-replace; boundary=frame",
    )


class SetCaptureModeRequest(BaseModel):
    mode: CaptureMode


class GetCaptureModeResponse(BaseModel):
    mode: CaptureMode


@router.post("/mode")
def set_mode(request: SetCaptureModeRequest) -> None:
    context = get_context()
    context.media_controller.switch_mode(request.mode)


@router.get("/mode", response_model=GetCaptureModeResponse)
def get_mode() -> GetCaptureModeResponse:
    context = get_context()
    return GetCaptureModeResponse(
        mode=context.media_controller.mode,
    )
