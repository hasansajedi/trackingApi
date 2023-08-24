import graphene

BASE_SHIPMENT_GRAPHQL_QUERY = """
{ 
    shipments { 
        tracking_number 
        carrier 
        sender_address 
        receiver_address 
        SKU 
        status 
        articles { 
            article_name 
            article_quantity 
            article_price 
        } 
        receiver_location_weather { 
            error { 
                text 
            } 
            cityName 
            temperature 
            weatherDescription 
            lastUpdated 
            humidity 
            wind 
            feelsLike 
            uv 
            timestamp 
        } 
    } 
}
"""


class WeatherErrorType(graphene.ObjectType):
    text = graphene.String(required=False)


class WeatherResponseType(graphene.ObjectType):
    error = graphene.Field(WeatherErrorType, required=False)
    cityName = graphene.String()
    temperature = graphene.Float()
    weatherDescription = graphene.String()
    lastUpdated = graphene.String()
    humidity = graphene.Int()
    wind = graphene.Float()
    feelsLike = graphene.Float()
    uv = graphene.Int()
    timestamp = graphene.Int()

    def resolve_error(self, info):
        if self.error is None:
            return None
        return self.error


class ArticleType(graphene.ObjectType):
    article_name = graphene.String()
    article_quantity = graphene.Int()
    article_price = graphene.Float()


class ShipmentType(graphene.ObjectType):
    tracking_number = graphene.String()
    carrier = graphene.String()
    sender_address = graphene.String()
    receiver_address = graphene.String()
    articles = graphene.List(ArticleType)
    SKU = graphene.String()
    status = graphene.String()
    receiver_location_weather = graphene.Field(WeatherResponseType)


class ShipmentsQuery(graphene.ObjectType):
    shipments = graphene.List(ShipmentType)

    def resolve_shipments(self, info):
        return info.context.get("shipments_data", [])


graphql_schema = graphene.Schema(
    query=ShipmentsQuery,
    auto_camelcase=False,
)
