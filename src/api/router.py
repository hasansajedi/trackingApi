from fastapi import APIRouter

from src.api.shipment.api import shipment_router
from src.api.weather.api import weather_router

router = APIRouter()


router.include_router(shipment_router, prefix="/shipments")
router.include_router(weather_router, prefix="/weather")
