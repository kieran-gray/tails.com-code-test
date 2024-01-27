FROM python:3.11-slim-bullseye as builder

RUN apt-get -y update && pip install poetry poetry-plugin-export

COPY poetry.lock pyproject.toml ./

RUN poetry export --without-urls --without-hashes >> requirements.txt && \
    poetry export --without-urls --without-hashes --only dev >> requirements-dev.txt

FROM python:3.11-slim-bullseye as prod

WORKDIR /app

COPY --from=builder /requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-deps -r requirements.txt

COPY . .

ENV PYTHONPATH=/app

USER www-data

FROM prod as dev

WORKDIR /app

ENV PYTHONPATH=/app

USER root

COPY --from=builder /requirements-dev.txt requirements-dev.txt
RUN pip install --no-deps -r requirements-dev.txt
