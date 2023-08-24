import pytest

from src.api.weather.schemas.weather import WeatherEnvironmentVariables


@pytest.fixture
def default_weather_environment_variables():
    return WeatherEnvironmentVariables(
        WEATHER_API_KEY="test", WEATHER_API_BASE_URL="https://api.weather.com/"
    )
