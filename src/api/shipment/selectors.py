import pandas as pd
from typing import Dict

from fastapi import Depends
from fastapi_pagination import Page
from fastapi_pagination.paginator import paginate

from src.api.shipment.dependencies import ShipmentApiDependencies
from src.api.shipment.schemas.shipment import (
    ShipmentModel,
    ArticleModel,
    ShipmentEnvironmentVariables,
)
from src.api.weather.dependencies import WeatherApiDependencies
from src.api.weather.schemas.weather import WeatherEnvironmentVariables
from src.api.weather.services import get_weather_info
from src.utils.pagination import CustomParams


class GetShipmentDataHelper:
    """
    Helper class to retrieve shipment data from a CSV file.
    Provides methods to retrieve shipment data from a CSV file, extract unique shipments, and paginate the results.
    """

    _weather_api_variables: WeatherEnvironmentVariables = None

    @classmethod
    async def get_data_from_csv_file(
        cls,
        params: CustomParams = Depends(),
        search: str = None,
        variables: ShipmentEnvironmentVariables = Depends(
            ShipmentApiDependencies.get_environment_variables
        ),
    ) -> Page[ShipmentModel]:
        """
        Loads the data from the CSV file, filters it based on the search keyword, extracts unique shipments,
        and returns the paginated results.

        @:param params (CustomParams, optional): The pagination parameters.
        @:param search (str, optional): The search keyword to filter the data.
        @:param variables (ShipmentEnvironmentVariables, optional): The shipment environment variables.

        :return: Page[ShipmentModel]: The paginated list of shipment models.
        """
        cls._weather_api_variables = (
            await WeatherApiDependencies.get_environment_variables()
        )

        df = await cls._load_data(variables.CSV_DATA_PATH, search)
        df.receiver_address = df.receiver_address.fillna("")
        unique_shipments = await cls._get_unique_shipments(df)
        paginated_shipments = paginate(list(unique_shipments.values()), params)
        return paginated_shipments

    @classmethod
    async def _load_data(cls, csv_file_path: str, search_keyword: str = None):
        """
        Load shipment data from a CSV file.

        @:param csv_file_path: The path to the CSV file.
        @:param search_keyword: The search keyword to filter the data.
        :return: The DataFrame containing the shipment data.
        """
        df = pd.read_csv(csv_file_path)

        if not search_keyword:
            return df

        columns_to_search = ["tracking_number", "carrier"]
        mask = (
            df[columns_to_search]
            .apply(
                lambda x: x.astype(str).str.contains(
                    search_keyword, case=False, na=False
                )
            )
            .any(axis=1)
        )
        return df[mask]

    @classmethod
    async def _get_unique_shipments(cls, df: pd.DataFrame) -> Dict[str, ShipmentModel]:
        """
        Extract unique shipments from the CSV data.

        @:param df: The DataFrame containing shipment data.
        :return: A dictionary of unique shipments with tracking number as key.
        """
        unique_shipments = {}
        for _, row in df.iterrows():
            tracking_number = row["tracking_number"]
            if tracking_number in unique_shipments:
                article = await cls._extract_values_to_article_model(row)
                unique_shipments[tracking_number].articles.append(article)
            else:
                unique_shipments[
                    tracking_number
                ] = await cls._extract_values_to_shipment_model(row)

        return unique_shipments

    @classmethod
    async def _extract_values_to_article_model(cls, row: Dict) -> ArticleModel:
        """
        Extract values from a row in the CSV and create an ArticleModel.

        @:param row: The dictionary representing a row in the CSV.
        :return: The created ArticleModel.
        """
        article_name = row.get("article_name", None)
        article_quantity = int(row.get("article_quantity", None))
        article_price = float(row.get("article_price", None))

        article = ArticleModel(
            article_name=article_name,
            article_quantity=article_quantity,
            article_price=article_price,
        )
        return article

    @classmethod
    async def _extract_values_to_shipment_model(cls, row: Dict) -> ShipmentModel:
        """
        Extract values from a row in the CSV and create a ShipmentModel.

        @:param row: The dictionary representing a row in the CSV.
        :return: The created ShipmentModel.
        """
        article = await cls._extract_values_to_article_model(row)
        receiver_location_weather = await get_weather_info(
            row.get("receiver_address", None),
            cls._weather_api_variables.WEATHER_API_KEY,
            str(cls._weather_api_variables.WEATHER_API_BASE_URL),
        )
        shipment = ShipmentModel(
            tracking_number=row.get("tracking_number", None),
            carrier=row.get("carrier", None),
            sender_address=row.get("sender_address", None),
            receiver_address=row.get("receiver_address", None),
            SKU=row.get("SKU", None),
            status=row.get("status", None),
            articles=[article],
            receiver_location_weather=receiver_location_weather,
        )
        return shipment
