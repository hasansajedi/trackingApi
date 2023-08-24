from fastapi import Query

from fastapi_pagination import Params


class CustomParams(Params):
    def __init__(self, page: int = Query(1, ge=1), size: int = Query(10, ge=1)):
        super().__init__(page=page, size=size)
