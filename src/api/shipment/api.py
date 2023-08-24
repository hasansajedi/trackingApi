from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from starlette import status

from src.api.shipment.schemas.graphql_schema import (
    graphql_schema,
    BASE_SHIPMENT_GRAPHQL_QUERY,
)
from src.api.shipment.schemas.shipment import ShipmentModel
from src.api.shipment.selectors import GetShipmentDataHelper


shipment_router = APIRouter(
    tags=["shipments"],
    redirect_slashes=False,
)


@shipment_router.get(
    "/",
    description="Get list of possible shipments.",
    response_model=Page[ShipmentModel],
    status_code=status.HTTP_200_OK,
)
async def get_shipments_list(
    shipments_data: Page = Depends(GetShipmentDataHelper.get_data_from_csv_file),
):
    return shipments_data


@shipment_router.get("/graphql/")
async def get_shipments_list_graphql(
    query: str = None,
    shipments_data: Page = Depends(GetShipmentDataHelper.get_data_from_csv_file),
):
    if query is None:
        query = BASE_SHIPMENT_GRAPHQL_QUERY

    result = graphql_schema.execute(
        query, context_value={"shipments_data": shipments_data.items}
    )

    return result.data
