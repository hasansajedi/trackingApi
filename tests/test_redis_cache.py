import pytest


@pytest.mark.asyncio
async def test_get_cache_hit(redis_cache_mock):
    redis_cache_mock.get.return_value = {"key": "value"}

    result = await redis_cache_mock.get("test_key", response_model=None)
    assert result == {"key": "value"}


@pytest.mark.asyncio
async def test_get_cache_miss(redis_cache_mock):
    redis_cache_mock.get.return_value = None

    result = await redis_cache_mock.get("test_key", response_model=None)
    assert result is None


@pytest.mark.asyncio
async def test_set_cache(redis_cache_mock):
    redis_cache_mock.set.return_value = True

    await redis_cache_mock.set("test_key", {"key": "value"})

    redis_cache_mock.set.assert_called_once()


@pytest.mark.asyncio
async def test_delete_cache(redis_cache_mock):
    redis_cache_mock.delete.return_value = True

    await redis_cache_mock.delete("test_key")

    redis_cache_mock.delete.assert_called_once_with("test_key")
