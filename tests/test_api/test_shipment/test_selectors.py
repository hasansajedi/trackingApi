import pandas as pd
import pytest

from src.api.shipment.schemas.shipment import ShipmentModel
from src.api.weather.schemas.weather import WeatherEnvironmentVariables
from src.api.shipment.selectors import GetShipmentDataHelper
from src.utils.pagination import CustomParams


@pytest.fixture(autouse=True)
def load_requirements(set_weather_env_variables):
    pass


@pytest.mark.asyncio
async def test_get_data_from_csv_file(
    default_shipment_environment_variables_without_address,
):
    params = CustomParams(page=1, size=2)
    response = await GetShipmentDataHelper.get_data_from_csv_file(
        params=params,
        variables=default_shipment_environment_variables_without_address,
    )
    assert response.total == 5
    assert response.page == 1
    assert response.pages == 3
    assert len(response.items) == 2


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "search_keyword, total, pages_count, items_count, article_count",
    [
        ("TN12345678", 1, 1, 1, 3),
        ("TN12345682", 1, 1, 1, 1),
        ("invalidSearchValue", 0, 0, 0, 0),
    ],
)
async def test_get_data_from_csv_file_with_search(
    default_shipment_environment_variables_without_address,
    search_keyword,
    total,
    pages_count,
    items_count,
    article_count,
):
    params = CustomParams(page=1, size=10)
    response = await GetShipmentDataHelper.get_data_from_csv_file(
        params=params,
        variables=default_shipment_environment_variables_without_address,
        search=search_keyword,
    )
    assert response.total == total
    assert response.pages == pages_count
    assert len(response.items) == items_count
    if total:
        assert len(response.items[0].articles) == article_count
        assert response.items[0].receiver_location_weather


@pytest.fixture
def shipment_data():
    data = {
        "tracking_number": ["T001", "T002", "T001"],
        "carrier": ["Carrier A", "Carrier B", "Carrier A"],
        "sender_address": ["Address A", "Address B", "Address A"],
        "receiver_address": ["Address X", "Address Y", "Address X"],
        "SKU": ["SKU001", "SKU002", "SKU001"],
        "status": ["Delivered", "In Transit", "Delivered"],
        "article_name": ["Article 1", "Article 2", "Article 3"],
        "article_quantity": [2, 1, 3],
        "article_price": [10.0, 5.0, 15.0],
    }
    return pd.DataFrame(data)


@pytest.mark.asyncio
async def test_get_unique_shipments(
    shipment_data, set_shipments_without_address_csv_file_path
):
    GetShipmentDataHelper._weather_api_variables = WeatherEnvironmentVariables(
        WEATHER_API_KEY="test", WEATHER_API_BASE_URL="https://api.weather.com/"
    )
    shipments = await GetShipmentDataHelper._get_unique_shipments(shipment_data)
    assert len(shipments) == 2
    assert "T001" in shipments
    assert "T002" in shipments
    assert shipments["T001"].tracking_number == "T001"
    assert shipments["T002"].tracking_number == "T002"
    assert shipments["T001"].articles[0].article_name == "Article 1"
    assert shipments["T001"].articles[0].article_quantity == 2
    assert shipments["T002"].articles[0].article_name == "Article 2"
    assert shipments["T002"].articles[0].article_quantity == 1


@pytest.mark.asyncio
async def test_extract_values_to_shipment_model(
    set_shipments_without_address_csv_file_path,
):
    row = {
        "tracking_number": "T001",
        "carrier": "Carrier A",
        "sender_address": "Address A",
        "receiver_address": "Address X",
        "SKU": "SKU001",
        "status": "Delivered",
        "article_name": "Article 1",
        "article_quantity": 2,
        "article_price": 10.0,
    }
    GetShipmentDataHelper._weather_api_variables = WeatherEnvironmentVariables(
        WEATHER_API_KEY="test", WEATHER_API_BASE_URL="https://api.weather.com/"
    )
    shipment: ShipmentModel = (
        await GetShipmentDataHelper._extract_values_to_shipment_model(row)
    )
    assert shipment.tracking_number == "T001"
    assert shipment.carrier == "Carrier A"
    assert shipment.sender_address == "Address A"
    assert shipment.receiver_address == "Address X"
    assert shipment.SKU == "SKU001"
    assert shipment.status == "Delivered"
    assert len(shipment.articles) == 1
    assert shipment.articles[0].article_name == "Article 1"
    assert shipment.articles[0].article_quantity == 2
    assert shipment.articles[0].article_price == 10.0


@pytest.mark.asyncio
async def test_extract_values_to_article_model():
    row = {
        "article_name": "Article 1",
        "article_quantity": 2,
        "article_price": 10.0,
    }
    GetShipmentDataHelper._weather_api_variables = WeatherEnvironmentVariables(
        WEATHER_API_KEY="test", WEATHER_API_BASE_URL="https://api.weather.com/"
    )
    article = await GetShipmentDataHelper._extract_values_to_article_model(row)
    assert article.article_name == "Article 1"
    assert article.article_quantity == 2
    assert article.article_price == 10.0


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "search_keyword, expected_count", [(None, 9), ("TN12345678", 3), ("invalid", 0)]
)
async def test_load_data(
    default_shipment_environment_variables, search_keyword, expected_count
):
    df = await GetShipmentDataHelper._load_data(
        default_shipment_environment_variables.CSV_DATA_PATH,
        search_keyword=search_keyword,
    )
    assert len(df) == expected_count
