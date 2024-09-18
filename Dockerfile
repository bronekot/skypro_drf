FROM python:3.12-slim

RUN pip install poetry && poetry config virtualenvs.create false

WORKDIR /app
COPY pyproject.toml poetry.lock /app/

RUN poetry install --no-interaction --no-ansi --no-dev --no-root

COPY . /app
