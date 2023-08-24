from fastapi import Request, Response

from src.utils.logging import logger


async def logging_middleware(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response: Response = await call_next(request)
    logger.info(f"Response: {response.status_code}")
    return response
