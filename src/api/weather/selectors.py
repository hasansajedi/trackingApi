from src.api.weather.schemas.weather import CurrentWeatherResponse, WeatherErrorResponse


def address_is_invalid(address: str, message: str = None) -> CurrentWeatherResponse:
    return CurrentWeatherResponse(
        error=WeatherErrorResponse(
            text=message or f"The address `{address}` cannot be reached."
        )
    )
