import functools
import json
from datetime import timedelta

from src.api.dependencies.redis_cache import redis_cache_helper


def cache_decorator(response_model, expire_time: timedelta):
    def decorator_cache_object(func):
        @functools.wraps(func)
        async def wrapper_cache_object(*args, **kwargs):
            key = f"{func.__name__}:{json.dumps(args)}:{json.dumps(kwargs)}"
            if kwargs.get("drop_key", False):
                await redis_cache_helper.delete(key)
            else:
                if cached_object := await redis_cache_helper.get(
                    key=key,
                    response_model=response_model,
                ):
                    return cached_object

            response = await func(*args, **kwargs)

            await redis_cache_helper.set(name=key, value=response, expiration_time=expire_time)
            return response

        return wrapper_cache_object

    return decorator_cache_object
