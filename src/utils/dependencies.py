import os
from typing import List

from fastapi import HTTPException
from starlette import status


class EnvironmentVariablesDependencies:
    _variables: List[str] = []
    _response_model = None

    @classmethod
    async def get_environment_variables(cls):
        missing_variables = []
        variables = {}
        for var_name in cls._variables:
            if os.getenv(var_name) is None or os.getenv(var_name) == "":
                missing_variables.append(var_name)
            else:
                variables[var_name] = os.getenv(var_name)

        if missing_variables:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"The following environment variables are missing or empty: {', '.join(missing_variables)}",
            )

        return cls._response_model(**variables)
