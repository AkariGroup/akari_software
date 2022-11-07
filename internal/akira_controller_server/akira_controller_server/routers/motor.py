from akari_client.joint_manager import AkariJoint
from fastapi import APIRouter
from pydantic import BaseModel

from ._context import get_context

router = APIRouter()


class GetServoStatusResponse(BaseModel):
    enabled: bool
    pan_min: float
    pan_max: float
    tilt_min: float
    tilt_max: float
    vel: float
    acc: float


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
    pan_min, pan_max = client.joints.pan_joint.get_position_limit()
    tilt_min, tilt_max = client.joints.tilt_joint.get_position_limit()
    vel = client.joints.pan_joint.get_profile_velocity()
    acc = client.joints.pan_joint.get_profile_acceleration()
    return GetServoStatusResponse(
        enabled=pan_servo and tilt_servo,
        pan_min=pan_min,
        pan_max=pan_max,
        tilt_min=tilt_min,
        tilt_max=tilt_max,
        vel=vel,
        acc=acc,
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


@router.post("/velocity")
def set_velocity(vel: float) -> None:
    context = get_context()
    client = context.akari_client

    client.joints.set_joint_velocities(
        pan=vel,
        tilt=vel,
    )


@router.post("/acceleration")
def set_acceleration(acc: float) -> None:
    context = get_context()
    client = context.akari_client

    client.joints.set_joint_accelerations(
        pan=acc,
        tilt=acc,
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
