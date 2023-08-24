import pytest


@pytest.fixture(autouse=True)
def load_requirements(set_weather_env_variables, redis_cache_mock):
    pass


@pytest.mark.asyncio
async def test_get_shipments_list(
    api_client, set_shipments_without_address_csv_file_path
):
    response = api_client.get("/api/shipments/")
    assert response.status_code == 200
    assert response.json()["total"] == 5
    assert response.json()["page"] == 1
    assert response.json()["pages"] == 1
    assert len(response.json()["items"]) == 5
    assert len(response.json()["items"][0]["articles"]) == 3


@pytest.mark.asyncio
async def test_get_shipments_empty_list(api_client, set_shipments_empty_csv_file_path):
    response = api_client.get("/api/shipments/")
    assert response.status_code == 200
    assert response.json()["total"] == 0
    assert response.json()["page"] == 1
    assert response.json()["pages"] == 0
    assert len(response.json()["items"]) == 0


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "page, page_size, pages, article_count", [(1, 2, 3, 3), (2, 1, 5, 1)]
)
async def test_get_shipments_list_paginated(
    api_client,
    set_shipments_without_address_csv_file_path,
    page,
    page_size,
    pages,
    article_count,
):
    response = api_client.get(f"/api/shipments/?page={page}&size={page_size}")
    assert response.status_code == 200
    assert response.json()["total"] == 5
    assert response.json()["page"] == page
    assert response.json()["pages"] == pages
    assert len(response.json()["items"]) == page_size
    assert len(response.json()["items"][0]["articles"]) == article_count


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "search_keyword, total, pages_count, items_count, article_count",
    [
        ("TN12345678", 1, 1, 1, 3),
        ("TN12345682", 1, 1, 1, 1),
        ("invalidSearchValue", 0, 1, 0, 0),
    ],
)
async def test_get_shipments_list_paginated(
    api_client,
    set_shipments_without_address_csv_file_path,
    search_keyword,
    total,
    pages_count,
    items_count,
    article_count,
):
    response = api_client.get(f"/api/shipments/?search={search_keyword}")
    assert response.status_code == 200
    assert response.json()["total"] == total
    assert response.json()["page"] == pages_count
    assert len(response.json()["items"]) == items_count
    if total:
        assert len(response.json()["items"][0]["articles"]) == article_count
        assert len(response.json()["items"][0]["receiver_location_weather"])


@pytest.mark.asyncio
async def test_get_shipments_list_graphql(
    api_client, set_shipments_without_address_csv_file_path
):
    response = api_client.get("/api/shipments/graphql/")
    assert response.status_code == 200
    assert len(response.json()["shipments"]) == 5
    assert len(response.json()["shipments"][0]["articles"]) == 3


@pytest.mark.asyncio
async def test_get_shipments_empty_list_graphql(
    api_client, set_shipments_empty_csv_file_path
):
    response = api_client.get("/api/shipments/graphql/")
    assert response.status_code == 200
    assert len(response.json()["shipments"]) == 0


@pytest.mark.asyncio
@pytest.mark.parametrize("page, page_size, article_count", [(1, 2, 3), (2, 1, 1)])
async def test_get_shipments_list_paginated_graphql(
    api_client,
    set_shipments_without_address_csv_file_path,
    page,
    page_size,
    article_count,
):
    response = api_client.get(f"/api/shipments/graphql/?page={page}&size={page_size}")
    assert response.status_code == 200
    assert len(response.json()["shipments"]) == page_size
    assert len(response.json()["shipments"][0]["articles"]) == article_count


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "search_keyword, total, article_count",
    [
        ("TN12345678", 1, 3),
        ("TN12345682", 1, 1),
        ("invalidSearchValue", 0, 0),
    ],
)
async def test_get_shipments_list_paginated_graphql(
    api_client,
    set_shipments_without_address_csv_file_path,
    search_keyword,
    total,
    article_count,
):
    response = api_client.get(f"/api/shipments/graphql/?search={search_keyword}")
    assert response.status_code == 200
    assert len(response.json()["shipments"]) == total
    if article_count:
        assert len(response.json()["shipments"][0]["articles"]) == article_count
