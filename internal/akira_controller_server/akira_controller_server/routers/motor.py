from akari_client.joint_manager import AkariJoint
from fastapi import APIRouter
from pydantic import BaseModel

from ._context import get_context

router = APIRouter()


class GetServoStatusResponse(BaseModel):
    enabled: bool


class SetPositionsRequest(BaseModel):
    pan: float
    tilt: float


class GetPositionsResponse(BaseModel):
    pan: float
    tilt: float


@router.get("/servo", response_model=GetServoStatusResponse)
def get_servo_status() -> GetServoStatusResponse:
    context = get_context()
    client = context.akari_client

    pan_servo = client.joints.pan_joint.get_servo_enabled()
    tilt_servo = client.joints.tilt_joint.get_servo_enabled()
    return GetServoStatusResponse(
        enabled=pan_servo and tilt_servo,
    )


@router.post("/servo")
def set_servo_status(enabled: bool) -> None:
    context = get_context()
    client = context.akari_client

    if enabled:
        client.joints.enable_all_servo()
    else:
        client.joints.disable_all_servo()


@router.post("/positions")
def set_positions(request: SetPositionsRequest) -> None:
    context = get_context()
    client = context.akari_client

    client.joints.move_joint_positions(
        pan=request.pan,
        tilt=request.tilt,
    )


@router.get("/positions", response_model=GetPositionsResponse)
def get_positions() -> GetPositionsResponse:
    context = get_context()
    client = context.akari_client

    positions = client.joints.get_joint_positions()
    return GetPositionsResponse(
        pan=positions[AkariJoint.PAN],
        tilt=positions[AkariJoint.TILT],
    )
