import re
from datetime import timedelta
from typing import Optional

from src.api.dependencies.decorators import cache_decorator
from src.api.weather.dependencies import WeatherApiDependencies
from src.api.weather.helpers import WeatherApiHelper
from src.api.weather.schemas.weather import (
    WeatherEnvironmentVariables,
    CurrentWeatherResponse,
)
from src.api.weather.selectors import address_is_invalid


def is_valid_address(address: str) -> bool:
    """
    Check if the provided address has a valid format.
    The address should have the format: "Street Number, Postal_Code City, Country".

    :returns: bool: True if the address has a valid format, False otherwise.
    """
    address_pattern = (
        r"^\s*([^,]+)\s*,\s*(\d{4,}(?:[-\s]?\d{4,})?)\s*([^,]+)\s*,\s*([^,]+)\s*$"
    )
    match = re.match(address_pattern, address.strip())
    return bool(match)


async def extract_city_zip_code_and_country_from_address(
    validated_address: str,
) -> tuple:
    """
    Extract city, zip code, and country from the provided address.

    :returns: tuple: A tuple containing city name, zip code, and country name.
    """
    zip_code_pattern = r"\b\d{5}\b"
    city_country_pattern = r",\s*([\w\s]+),\s*([\w\s]+)$"

    zip_codes = re.findall(zip_code_pattern, validated_address)
    city_country = re.findall(city_country_pattern, validated_address)

    zip_code = zip_codes[0] if zip_codes else None
    if city_country:
        city_name, country_name = city_country[0]
        city_name = (
            city_name.split(" ")[1].strip()
            if len(city_name.split(" ")) > 1
            else city_name.strip()
        )
        country_name = country_name.strip()
    else:
        city_name, country_name = None, None

    return city_name, zip_code, country_name


@cache_decorator(
    response_model=CurrentWeatherResponse,
    expire_time=timedelta(seconds=5),
)
async def get_weather_info(
    address: str, weather_api_key: str, weather_api_url: str
) -> Optional[CurrentWeatherResponse]:
    """
    Get weather information for the provided address.
    Makes an API request to the external weather service to get the current weather information for the given address.

    :returns: Optional[CurrentWeatherResponse]: The weather information as a CurrentWeatherResponse object,
              or None if the address is invalid or the API request fails.
    """
    if not address or not is_valid_address(address):
        return address_is_invalid(address)

    city_name, zip_code, country = await extract_city_zip_code_and_country_from_address(
        validated_address=address
    )
    if (city_name or zip_code) and country:
        api_helper = WeatherApiHelper(address, city_name, zip_code, country)
        response = await api_helper.get_current_weather_response_from_api(
            weather_api_url,
            weather_api_key,
        )
        return response


async def get_current_weather(address: str) -> CurrentWeatherResponse:
    variables: WeatherEnvironmentVariables = (
        await WeatherApiDependencies.get_environment_variables()
    )
    return await get_weather_info(
        address, variables.WEATHER_API_KEY, str(variables.WEATHER_API_BASE_URL)
    )
