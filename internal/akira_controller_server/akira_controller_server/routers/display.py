from akari_client.color import Color
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ._context import get_context

router = APIRouter()


class ColorType(BaseModel):
    r: int
    g: int
    b: int

    def to_akari(self) -> Color:
        return Color(
            red=self.r,
            green=self.g,
            blue=self.b,
        )


class SetRequest(BaseModel):
    text: str
    bg_color: ColorType


@router.post("/values")
def set_values(request: SetRequest) -> None:
    context = get_context()
    client = context.akari_client

    try:
        bg_color = request.bg_color.to_akari()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"bad request: {e}")

    client.m5stack.set_display_text(
        text=request.text,
        back_color=bg_color,
    )
