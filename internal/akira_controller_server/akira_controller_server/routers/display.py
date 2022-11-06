from typing import Tuple

from akari_client.color import Color
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ._context import get_context

router = APIRouter()

ColorType = Tuple[int, int, int]


class SetRequest(BaseModel):
    text: str
    bg_color: ColorType


@router.post("/values")
def set_values(request: SetRequest) -> None:
    context = get_context()
    client = context.akari_client

    try:
        bg_color = Color(*request.bg_color)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"bad request: {e}")

    client.m5stack.set_display_text(
        text=request.text,
        back_color=bg_color,
    )
