from akari_client.joint_manager import AkariJoint
from fastapi import APIRouter
from pydantic import BaseModel

from ._context import get_context

router = APIRouter()


class SetPositionsRequest(BaseModel):
    pan: float
    tilt: float


class GetPositionsResponse(BaseModel):
    pan: float
    tilt: float


@router.post("/positions")
def set_positions(request: SetPositionsRequest) -> None:
    context = get_context()
    client = context.akari_client

    client.joints.move_joint_positions(
        pan=request.pan,
        tilt=request.tilt,
    )


@router.get("/positions")
def get_positions() -> GetPositionsResponse:
    context = get_context()
    client = context.akari_client

    positions = client.joints.get_joint_positions()
    return GetPositionsResponse(
        pan=positions[AkariJoint.PAN],
        tilt=positions[AkariJoint.TILT],
    )
