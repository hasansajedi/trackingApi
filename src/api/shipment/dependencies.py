from typing import List


from src.api.shipment.schemas.shipment import ShipmentEnvironmentVariables
from src.utils.dependencies import EnvironmentVariablesDependencies


class ShipmentApiDependencies(EnvironmentVariablesDependencies):
    _variables: List[str] = ["CSV_DATA_PATH"]
    _response_model = ShipmentEnvironmentVariables
