from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse

from src.api.dependencies.configuration import app_settings
from src.api.dependencies.redis_cache import redis_cache_helper
from src.api.router import router

app = FastAPI(
    title=app_settings.title,
    version=app_settings.version,
    description=app_settings.description,
    openapi_prefix=app_settings.openapi_prefix,
    docs_url=app_settings.docs_url,
    openapi_url=app_settings.openapi_url,
)

# prevent FastAPI from redirecting missing slashes to an HTTP version
app.router.redirect_slashes = False

# Import the routes from APIs
app.include_router(router, prefix=app_settings.api_prefix)


@app.on_event("startup")
async def startup_event():
    redis_client = redis_cache_helper
    if not redis_client:
        raise Exception("Redis client not configured correctly.")


@app.on_event("shutdown")
async def shutdown_event():
    if redis_cache_helper:
        await redis_cache_helper.close()


# Function to generate OpenAPI schema
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title, version=app.version, routes=app.routes
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


@app.get("/openapi.json", include_in_schema=False)
async def get_open_api_endpoint():
    return JSONResponse(content=custom_openapi())
