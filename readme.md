# Build 

## Start container

Installing and deploying in a Docker container is a straightforward process. 

By default, Docker exposes port 8000, but this value can be modified in the `docker-compose.yml` file if needed. Once you are ready, you can easily build the image using the Dockerfile.

The API comes with default configurations, which are listed here:

| Name                  | Reason to use                           |
|-----------------------|-----------------------------------------|
| REDIS_SERVER          | Connect to Redis.                       |
| REDIS_PORT            | Connect to Redis.                       |
| WEATHER_API_KEY       | The weather api key                     |
| WEATHER_API_BASE_URL  | The weather api URL                     |
| CACHE_TTL_IN_SECONDS  | The time to caching weather information |
| ENABLE_DOCUMENTATION  | True                                    |
| DEBUG                 | True                                    |


```shell
cd trackApi
docker-compose up -d --build
```

then you have to wait to installing requirements and deploying api. Once process finished, run:
```shell
.
.
.
 ✔ Container trackapi-cache-1         Running             0.0s 
 ✔ Container track_api                Started             1.5s 
```
to see which services already created, use:
```shell
> docker-compose ps

# result
|NAME                |IMAGE                |COMMAND                  |SERVICE             |CREATED             |STATUS              |                     
|--------------------|---------------------|-------------------------|--------------------|--------------------|--------------------|
|track_api           |trackapi-track_api   |"uvicorn --host 0.0.…"   |track_api           |2 minutes ago       |Up 2 minutes        |
|trackapi-cache-1    |redis:6.2-alpine     |"docker-entrypoint.s…"   |cache               |About an hour ago   |Up About an hour    |
```
to make sure api is started and ready to use, use:
```shell
> docker-compose logs track_api

# result
track_api  | 2023-08-05T14:46:24.392542610Z INFO:     Started server process [1]
track_api  | 2023-08-05T14:46:24.392559862Z INFO:     Waiting for application startup.
track_api  | 2023-08-05T14:46:24.418326974Z INFO:     Application startup complete.
track_api  | 2023-08-05T14:46:24.418696417Z INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```
### Run tests

```shell
docker-compose run track_api pytest tests/

# result
# 37 passed, 1 warnings in 0.86s
```
##
#### *Now api and database is ready to use.*

## API Endpoints

### Shipments 

#### Get List of Shipments

Get a paginated list of possible shipments.

- **URL:** `/api/shipments/`
- **Method:** GET
- **Query Parameters:**
  - `page`: Page number for pagination (optional)
  - `size`: Number of items per page (optional)
  - `search`: Search keyword to filter the data (optional)
- **Response:**
  - HTTP status code: 200 OK
  - Response body: Paginated list of shipment models
  ```json
  {
      "items":[
      {
          "tracking_number":"TN12345680",
          "carrier":"DPD",
          "sender_address":"Street 3, 80331 Munich, Germany",
          "receiver_address":"Street 5, 28013 Madrid, Spain",
          "articles":[
              {
                  "article_name":"Keyboard",
                  "article_quantity":1,
                  "article_price":50.0
              },
              ...
          ],
          "SKU":"KB012",
          "status":"delivery",
          "receiver_location_weather":{
              "error":null,
              "cityName":"Madrid",
              "temperature":27.0,
              "weatherDescription":"Sunny",
              "lastUpdated":"2023-08-05 14:15",
              "humidity":25,
              "wind":6.1,
              "feelsLike":25.2,
              "uv":9,
              "timestamp":1691238225
          }
      },
      ...
      ],
      "total":120,
      "page":2,
      "size":2,
      "pages":60
  }
  ```  

#### GraphQL API

Get a list of shipments using GraphQL.

- **URL:** `/api/shipments/graphql/`
- **Method:** GET
- **Query Parameters:**
  - `page`: Page number for pagination (optional)
  - `size`: Number of items per page (optional)
  - `search`: Search keyword to filter the data (optional)
  - `query`: GraphQL query string (optional, default query provided if not specified)
  ```json
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
  ```
- **Response:**
  - HTTP status code: 200 OK
  - Response body: Result of the GraphQL query with shipment data
  ```json
  {
      "shipments":[
      {
          "tracking_number":"TN12345680",
          "carrier":"DPD",
          "sender_address":"Street 3, 80331 Munich, Germany",
          "receiver_address":"Street 5, 28013 Madrid, Spain",
          "SKU":"KB012",
          "status":"delivery",
          "articles":[
              {
                  "article_name":"Keyboard",
                  "article_quantity":1,
                  "article_price":50.0
              },
              ...
          ],
          "receiver_location_weather":
          {
              "error":null,
              "cityName":"Madrid",
              "temperature":27.0,
              "weatherDescription":"Sunny",
              "lastUpdated":"2023-08-05 14:15",
              "humidity":25,
              "wind":6.1,
              "feelsLike":25.2,
              "uv":9,
              "timestamp":1691238225
          }
      },
      ...
      ]
  }
  ```
The value of query and result of response can be customized by client. That means if you put `query={shipments {tracking_number carrier sender_address receiver_address}}` to the end of your url, then the result would be like this:
```json
{
    "shipments":[
        {
            "tracking_number":"TN12345680",
            "carrier":"DPD",
            "sender_address":"Street 3, 80331 Munich, Germany",
            "receiver_address":"Street 5, 28013 Madrid, Spain"
        },
        {
            "tracking_number":"TN12345681",
            "carrier":"FedEx",
            "sender_address":"Street 4, 50667 Cologne, Germany",
            "receiver_address":"Street 9, 1016 Amsterdam, Netherlands"
        }
    ]
}
```

### Weather

#### Get Current Weather

Get the current weather for the provided address.

- **URL:** `/api/weather/current/{address}`
- **Method:** GET
- **Path Parameters:**
  - `address`: Address for which weather information is requested
  - `drop_key`: Remove cached weather information if `True` otherwise fetch from cache server.
- **Response:**
  - HTTP status code: 200 OK
  - Response body: Current weather information
  ```json
  {
      "error":null,
      "cityName":"Paris",
      "temperature":18.0,
      "weatherDescription":"Partly cloudy",
      "lastUpdated":"2023-08-05 13:45",
      "humidity":73,
      "wind":20.2,
      "feelsLike":18.0,
      "uv":4,
      "timestamp":1691236457
  }
  ```
  When the provided address is invalid (which does not following `Street Number, Postal_Code City, Country` format), the output will be :
  ```json
  {
      "error":{
          "text":"The address `InvalidAddress` cannot be reached."
      },
      "cityName":null,
      ...
  }
  ```
## Environment Variables

The backend server relies on the following environment variables. Make sure to set them before running the server:

- `WEATHER_API_KEY`: API key for the weather API.
- `WEATHER_API_BASE_URL`: Base URL for the weather API.
- `CSV_DATA_PATH`: Path to the CSV file containing shipment data.

## Libraries

| Name               | Reason to use                                                                 |
|--------------------|-------------------------------------------------------------------------------|
| Black              | To reformatting Python codes.                                                 |
| pandas             | To fetch data from CSV file and perform some correction.                      |
| pydantic           | To validating data and making custom transparent models.                      |
| graphene           | To fetch data based on GraphQL schema.                                        |
| fastapi-pagination | To enable pagination in the HTTP responses.                                   |
| httpx              | To call external Api which supports Async request.                            |
| redis              | To use as cache server to caching weather information based on given address. |


> **Possible endpoints:**
> 
> Possible endpoints listed in `test_main.http` file.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
