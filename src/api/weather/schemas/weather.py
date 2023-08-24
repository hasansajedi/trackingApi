from typing import Optional, Union

from pydantic import BaseModel, HttpUrl, Field, field_validator


class WeatherEnvironmentVariables(BaseModel):
    WEATHER_API_KEY: str
    WEATHER_API_BASE_URL: HttpUrl


class WeatherErrorResponse(BaseModel):
    text: str

    @field_validator("text")
    def set_receiver_location_weather(cls, text):
        if not text:
            return ""
        return text


class CurrentWeatherResponse(BaseModel):
    error: Optional[WeatherErrorResponse] = Field(default=None)
    cityName: str = Field(default=None)
    temperature: float = Field(default=None)
    weatherDescription: str = Field(default=None)
    lastUpdated: str = Field(default=None)
    humidity: int = Field(default=None)
    wind: Union[float, int] = Field(default=None)
    feelsLike: float = Field(default=None)
    uv: int = Field(default=None)
    timestamp: int = Field(default=None)
