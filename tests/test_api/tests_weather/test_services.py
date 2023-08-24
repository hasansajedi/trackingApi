import re

import pytest
from aioresponses import aioresponses

from src.api.weather.helpers import WeatherApiHelper
from src.api.weather.schemas.weather import (
    CurrentWeatherResponse,
)
from src.api.weather.services import (
    is_valid_address,
    extract_city_zip_code_and_country_from_address,
    get_weather_info,
    get_current_weather,
)


@pytest.mark.parametrize(
    "address, is_valid",
    [
        ("invalid address", False),
        ("Street 10, 75001, France", True),
        ("Street 10, 75001 Paris, France", True),
        ("1234 Elm Street, 56789 Springfield, USA", True),
    ],
)
def test_is_valid_address(address, is_valid):
    assert is_valid_address(address) == is_valid


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "address, expected_city_name, expected_zip_code, expected_country_name",
    [
        ("invalid address", None, None, None),
        ("Street 10, 75001, France", "75001", "75001", "France"),
        ("Street 10, 75001 Paris, France", "Paris", "75001", "France"),
        ("1234 Elm Street, 56789 Springfield, USA", "Springfield", "56789", "USA"),
    ],
)
async def test_extract_city_zip_code_and_country_from_address(
    address, expected_city_name, expected_zip_code, expected_country_name
):
    (
        city_name,
        zip_code,
        country_name,
    ) = await extract_city_zip_code_and_country_from_address(address)
    assert city_name == expected_city_name
    assert zip_code == expected_zip_code
    assert country_name == expected_country_name


@pytest.mark.asyncio
async def test_get_weather_info_valid():
    address = "Street 10, 40667 Meerbuch, Germany"
    with aioresponses() as mocked:
        mocked.get(
            re.compile(r"https://api\.weather\.com/.*"),
            payload={
                "location": {"name": "Meerbuch"},
                "current": {
                    "temp_c": 22.5,
                    "last_updated": "2023-07-31 12:00",
                    "humidity": 60,
                    "wind_kph": 10.2,
                    "feelslike_c": 24.0,
                    "uv": 5,
                    "condition": {"text": "Partly cloudy"},
                },
            },
            status=200,
        )
        api_helper = WeatherApiHelper(address, "Meerbuch", "40667", "Germany")
        response = await api_helper.get_current_weather_response_from_api(
            weather_api_key="test_key",
            weather_api_url="https://api.weather.com/",
        )
        assert isinstance(response, CurrentWeatherResponse)


@pytest.mark.asyncio
async def test_get_weather_info_invalid():
    invalid_address = "Invalid Address"
    response = await get_weather_info(
        invalid_address,
        weather_api_key="test_key",
        weather_api_url="https://api.weather.com/",
    )
    assert response.error.text == "The address `Invalid Address` cannot be reached."
    assert not response.cityName


@pytest.mark.asyncio
async def test_get_current_weather_valid(default_weather_environment_variables):
    address = "Street 10, 40667 Meerbuch, Germany"
    with aioresponses() as mocked:
        mocked.get(
            re.compile(r"https://api\.weather\.com/.*"),
            payload={
                "location": {"name": "Meerbuch"},
                "current": {
                    "temp_c": 22.5,
                    "last_updated": "2023-07-31 12:00",
                    "humidity": 60,
                    "wind_kph": 10.2,
                    "feelslike_c": 24.0,
                    "uv": 5,
                    "condition": {"text": "Partly cloudy"},
                },
            },
            status=200,
        )
        response = await get_current_weather(address)
        assert isinstance(response, CurrentWeatherResponse)


@pytest.mark.asyncio
async def test_get_current_weather_invalid(default_weather_environment_variables):
    invalid_address = "Invalid Address"
    response = await get_current_weather(invalid_address)
    assert response.error.text == "The address `Invalid Address` cannot be reached."
    assert not response.cityName
