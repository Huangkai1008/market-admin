FROM python:3.7.5-slim-stretch

RUN apt-get update \
    && apt-get install -y gcc

EXPOSE 8000
WORKDIR /app

COPY poetry.lock pyproject.toml ./
RUN pip install poetry \
    && poetry config settings.virtualenvs.create false \
    && poetry install --no-dev

COPY . ./

CMD uvicorn --host=0.0.0.0 app.main:app
