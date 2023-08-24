import os

from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()


class AppGlobalConfigModel(BaseModel):
    title: str = Field(default=os.environ.get("TITLE"))
    version: str = "1.0.0"
    description: str = Field(default=os.environ.get("DESCRIPTION"))
    openapi_prefix: str = "/openapi"
    docs_url: str = "/docs"
    redoc_url: str = "/redoc"
    openapi_url: str = "/openapi.json"
    api_prefix: str = "/api"
    debug: bool = Field(default=bool(os.environ.get("DEBUG")))
    redis_server: str = Field(default=os.environ.get("REDIS_SERVER"))
    redis_port: int = Field(default=int(os.environ.get("REDIS_PORT")))
    redis_cache_expiration_time_in_sec: int = Field(
        default=int(os.environ.get("CACHE_TTL_IN_SECONDS", 7200))
    )


app_settings = AppGlobalConfigModel()
