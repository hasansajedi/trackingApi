from typing import List

from src.api.weather.schemas.weather import WeatherEnvironmentVariables
from src.utils.dependencies import EnvironmentVariablesDependencies


class WeatherApiDependencies(EnvironmentVariablesDependencies):
    _variables: List[str] = ["WEATHER_API_KEY", "WEATHER_API_BASE_URL"]
    _response_model = WeatherEnvironmentVariables
