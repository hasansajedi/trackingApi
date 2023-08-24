from unittest.mock import AsyncMock, patch

import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient

from src.api.dependencies.configuration import app_settings
from src.api.dependencies.redis_cache import redis_cache_helper, RediCacheHelper
from src.main import app


@pytest.fixture
def default_app() -> FastAPI:
    return app


@pytest.fixture
def api_client(default_app) -> TestClient:
    client = TestClient(default_app)
    return client


@pytest.fixture
def set_weather_env_variables(monkeypatch):
    monkeypatch.setenv("WEATHER_API_KEY", "20f6a3489c5047249b324b5f6c34e8ca")
    monkeypatch.setenv("WEATHER_API_BASE_URL", "https://api.weatherbit.io/v2.0/current")
    monkeypatch.setenv("REDIS_SERVER", "localhost")
    monkeypatch.setenv("REDIS_PORT", "6333")
    monkeypatch.setenv("CACHE_TTL_IN_SECONDS", "2")
    monkeypatch.setenv("CSV_DATA_PATH", "data/shipments.csv")


@pytest.fixture(autouse=True)
def default_settings():
    return app_settings


@pytest.fixture
def redis_cache_mock(default_settings):
    with patch(
        "src.api.dependencies.redis_cache.redis_cache_helper", spec=RediCacheHelper
    ) as mock:
        mock.get = AsyncMock()
        mock.set = AsyncMock()
        mock.delete = AsyncMock()
        yield mock
