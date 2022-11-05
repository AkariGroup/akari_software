from fastapi import APIRouter
from pydantic import BaseModel

from ._context import get_context

router = APIRouter()


class GetValuesResponse(BaseModel):
    button_a: bool
    button_b: bool
    button_c: bool
    din0: bool
    din1: bool
    ain0: int
    temperature: float
    pressure: float
    brightness: int


@router.get("/values")
def get_values() -> GetValuesResponse:
    context = get_context()
    client = context.akari_client

    values = client.m5stack.get()
    return GetValuesResponse(
        button_a=values["button_a"],
        button_b=values["button_b"],
        button_c=values["button_c"],
        din0=values["din0"],
        din1=values["din1"],
        ain0=values["ain0"],
        temperature=values["temperature"],
        pressure=values["pressure"],
        brightness=values["brightness"],
    )
