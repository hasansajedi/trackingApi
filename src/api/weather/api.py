from datetime import timedelta
from typing import Optional

from fastapi import APIRouter

from starlette import status

from src.api.dependencies.configuration import app_settings
from src.api.dependencies.decorators import cache_decorator
from src.api.weather.schemas.weather import (
    CurrentWeatherResponse,
)
from src.api.weather.services import get_current_weather

weather_router = APIRouter(
    tags=["weather"],
    redirect_slashes=False,
)


@weather_router.get(
    "/current/{address}",
    description="Get the current weather for the provided address.",
    response_model=Optional[CurrentWeatherResponse],
    status_code=status.HTTP_200_OK,
)
@cache_decorator(
    response_model=CurrentWeatherResponse,
    expire_time=timedelta(seconds=app_settings.redis_cache_expiration_time_in_sec),
)
async def get_weather(address: str, drop_key: bool = False):
    return await get_current_weather(address)
