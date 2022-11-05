from fastapi import APIRouter
from pydantic import BaseModel

from ._context import get_context

router = APIRouter()


class SetRequest(BaseModel):
    dout0: bool
    dout1: bool
    pwmout0: int


@router.post("/values")
def set_values(request: SetRequest) -> None:
    context = get_context()
    client = context.akari_client

    client.m5stack.set_allout(
        dout0=request.dout0,
        dout1=request.dout1,
        pwmout0=request.pwmout0,
    )
