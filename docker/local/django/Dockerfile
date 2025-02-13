FROM python:3.12-slim as python

ARG APP_HOME=/app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV POETRY_VERSION 2.0.1

WORKDIR ${APP_HOME}

# Install required system dependencies
RUN apt update && apt install --no-install-recommends -y \
  wait-for-it \
  # psycopg2 dependencies
  libpq-dev \
  python3-dev \
  build-essential \
  # Translations dependencies
  gettext \
  # cleaning up unused files
  && apt purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# install poetry
RUN pip install poetry==$POETRY_VERSION

# install dependencies
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false && \
    poetry install --with dev --no-root

COPY ./docker/local/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static

COPY . ${APP_HOME}

ENTRYPOINT ["/start"]
