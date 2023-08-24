import time
from typing import Dict, Any

from httpx import AsyncClient, Response
from starlette import status

from src.api.dependencies.redis_cache import redis_cache_helper
from src.api.weather.schemas.weather import CurrentWeatherResponse
from src.api.weather.selectors import address_is_invalid
from src.utils.logging import logger


class WeatherApiHelper:
    _address: str
    _zip_code: str
    _country: str
    _city_name: str

    def __init__(
        self,
        address: str,
        city_name: str,
        zip_code: str,
        country: str,
    ):
        self._address = address
        self._zip_code = zip_code
        self._country = country
        self._city_name = city_name

    async def get_current_weather_response_from_api(
        self,
        weather_api_url: str,
        weather_api_key: str,
    ):
        async with AsyncClient() as client:
            response = await client.get(
                weather_api_url,
                params={
                    "q": self._city_name,
                    "aqi": "no",
                    "key": weather_api_key,
                },
            )
            if err := self._validate_response(response):
                return err

            weather_data = self._process_response(response.json())
            return CurrentWeatherResponse(**weather_data)

    def _validate_response(self, response: Response) -> CurrentWeatherResponse:
        if not response.content:
            return address_is_invalid(
                self._address,
                message="The response is not valid.",
            )

        if response.status_code == status.HTTP_429_TOO_MANY_REQUESTS:
            return address_is_invalid(
                self._address,
                message="The weather API throttled, please try again later.",
            )
        elif response.status_code != status.HTTP_200_OK:
            return address_is_invalid(self._address)

    def _process_response(self, weather_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "cityName": weather_data["location"]["name"],
            "temperature": weather_data["current"]["temp_c"],
            "lastUpdated": weather_data["current"]["last_updated"],
            "humidity": weather_data["current"]["humidity"],
            "wind": weather_data["current"]["wind_kph"],
            "feelsLike": weather_data["current"]["feelslike_c"],
            "uv": weather_data["current"]["uv"],
            "weatherDescription": weather_data["current"]["condition"]["text"],
            "timestamp": int(time.time()),
        }
