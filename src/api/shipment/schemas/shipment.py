from typing import List, Optional

from pydantic import BaseModel, field_validator

from src.api.weather.schemas.weather import CurrentWeatherResponse, WeatherErrorResponse


class ShipmentEnvironmentVariables(BaseModel):
    CSV_DATA_PATH: str


class BaseListResponse(BaseModel):
    count: int
    next: Optional[str]
    previous: Optional[str]


class ArticleModel(BaseModel):
    article_name: str
    article_quantity: int
    article_price: float


class ShipmentModel(BaseModel):
    tracking_number: str
    carrier: str
    sender_address: str
    receiver_address: Optional[str]
    articles: List[ArticleModel]
    SKU: str
    status: str
    receiver_location_weather: Optional[CurrentWeatherResponse]

    @field_validator("receiver_location_weather")
    def set_receiver_location_weather(cls, receiver_location_weather, values):
        if receiver_location_weather:
            return receiver_location_weather
        return CurrentWeatherResponse(
            error=WeatherErrorResponse(
                text=f"The address `{values.get('receiver_address', '')}` cannot be reached."
            )
        )


class ShipmentListResponse(BaseListResponse):
    results: List[Optional[ShipmentModel]]
