import pytest

from src.api.shipment.schemas.shipment import ShipmentEnvironmentVariables


@pytest.fixture
def default_shipment_environment_variables():
    return ShipmentEnvironmentVariables(CSV_DATA_PATH="tests/data/shipments.csv")


@pytest.fixture
def default_shipment_environment_variables_without_address():
    return ShipmentEnvironmentVariables(
        CSV_DATA_PATH="tests/data/shipments_without_address.csv"
    )


@pytest.fixture
def set_shipments_without_address_csv_file_path(monkeypatch):
    monkeypatch.setenv("CSV_DATA_PATH", "tests/data/shipments_without_address.csv")


@pytest.fixture
def set_shipments_empty_csv_file_path(monkeypatch):
    monkeypatch.setenv("CSV_DATA_PATH", "tests/data/shipments_empty.csv")
