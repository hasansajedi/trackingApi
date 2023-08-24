FROM python:3.11-bullseye as python-base

FROM python-base as poetry

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry export -f requirements.txt --without-hashes -o requirements.txt
RUN poetry export -f requirements.txt --dev --without-hashes -o dev_requirements.txt

FROM python-base as api-base

LABEL description="Tracking Shipments API"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ARG WEATHER_API_KEY
ARG WEATHER_API_BASE_URL
ARG CACHE_TTL_IN_SECONDS
ARG ENABLE_DOCUMENTATION
ARG DEBUG

ENV WEATHER_API_KEY=$WEATHER_API_KEY
ENV WEATHER_API_BASE_URL=$WEATHER_API_BASE_URL
ENV CACHE_TTL_IN_SECONDS=$CACHE_TTL_IN_SECONDS
ENV ENABLE_DOCUMENTATION=$ENABLE_DOCUMENTATION
ENV DEBUG=$DEBUG

LABEL WEATHER_API_KEY=$WEATHER_API_KEY
LABEL WEATHER_API_BASE_URL=$WEATHER_API_BASE_URL
LABEL CACHE_TTL_IN_SECONDS=$CACHE_TTL_IN_SECONDS
LABEL ENABLE_DOCUMENTATION=$ENABLE_DOCUMENTATION
LABEL DEBUG=$DEBUG

ENV APP /workspace

RUN apt-get update

RUN mkdir -p $APP
WORKDIR $APP

COPY --from=poetry requirements.txt .
RUN pip install --no-cache-dir --no-deps -r requirements.txt

COPY . .

FROM api-base as test-env

COPY --from=poetry dev_requirements.txt .
RUN pip install --no-cache-dir --no-deps -r dev_requirements.txt

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8000", "src.main:app"]
