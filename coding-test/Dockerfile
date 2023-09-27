FROM python:3.11-slim-bullseye

RUN apt-get -y update && pip install pipenv
WORKDIR /app

RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH" VIRTUAL_ENV="/venv" PYTHONPATH="."

COPY Pipfile Pipfile.lock /app/
RUN pipenv install
COPY . .

EXPOSE 5000
