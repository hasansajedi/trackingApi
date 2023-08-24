import pytest

from src.api.weather.services import get_current_weather


async def mock_get_current_weather(address: str):
    return {"cityName": "Berlin", "temperature": 15.5}


@pytest.fixture
def override_get_current_weather(default_app):
    default_app.dependency_overrides[get_current_weather] = mock_get_current_weather
    yield
    default_app.dependency_overrides.pop(get_current_weather)


def test_get_weather_valid_address(
    default_weather_environment_variables,
    set_weather_env_variables,
    api_client,
    override_get_current_weather,
    redis_cache_mock,
):
    address = "Street 10, 75001 Paris, France"
    response = api_client.get(f"/api/weather/current/{address}")

    assert response.status_code == 200
    assert "cityName" in response.json()
    assert "temperature" in response.json()
