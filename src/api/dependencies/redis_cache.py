import pickle
from datetime import timedelta
from typing import Any, Awaitable, Type, Union, Optional

from pydantic.main import BaseModel
from redis.asyncio.client import Redis
from redis.typing import KeyT, EncodableT

from src.api.dependencies.configuration import app_settings
from src.utils.logging import logger


class RediCacheHelper(Redis):
    async def get(self, key: str = "cache_prefix", response_model=None) -> Any:
        try:
            if cached_object := await super().get(name=key):
                logger.info(f"Use cached result for `{key}` key.")
                result = pickle.loads(cached_object)
                if isinstance(result, dict):
                    return response_model(**result)
                return result
            return None
        except:
            return None

    async def set(
        self,
        name: KeyT,
        value: Union[EncodableT, Type[BaseModel]],
        expiration_time: timedelta = app_settings.redis_cache_expiration_time_in_sec,
    ) -> Awaitable:
        try:
            return await super().set(
                name=name,
                value=pickle.dumps(value),
                ex=expiration_time,
                nx=False,
                xx=False,
                keepttl=False,
            )
        except:
            return None

    async def delete(self, key: str) -> Optional[int]:
        return await super().delete(key)


redis_cache_helper = RediCacheHelper(
    host=app_settings.redis_server, port=app_settings.redis_port
)
