from fastapi import APIRouter

from .routers.camera import router as CameraRouter
from .routers.display import router as DisplayRouter
from .routers.motor import router as MotorRouter
from .routers.pinout import router as PinoutRouter
from .routers.sensors import router as SensorRouter

api = APIRouter()
api.include_router(CameraRouter, prefix="/camera")
api.include_router(DisplayRouter, prefix="/display")
api.include_router(MotorRouter, prefix="/motor")
api.include_router(PinoutRouter, prefix="/pinout")
api.include_router(SensorRouter, prefix="/sensor")
