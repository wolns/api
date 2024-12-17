FROM python:3.12-slim

EXPOSE 8000

RUN pip install --no-cache-dir poetry

WORKDIR /wolns-api

COPY pyproject.toml ./

RUN poetry install

COPY . ./

CMD poetry run alembic upgrade head && poetry run gunicorn src:create_app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:2000