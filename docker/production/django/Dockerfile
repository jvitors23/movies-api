FROM python:3.12 as python

ARG APP_HOME=/app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV POETRY_VERSION 2.0.1

WORKDIR ${APP_HOME}

RUN addgroup --system django \
    && adduser --system --ingroup django django

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
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/* \

# install poetry
RUN pip install poetry==$POETRY_VERSION

#install dependencies
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false && \
    poetry install --without dev --no-root

COPY --chown=django:django ./docker/production/django/start /start

RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

# copy application code to WORKDIR
COPY --chown=django:django . ${APP_HOME}

# make django owner of the WORKDIR directory as well.
RUN chown django:django ${APP_HOME}

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static

RUN chown django:django /vol/web/media
RUN chown django:django /vol/web/static

EXPOSE 8000

USER django

ENTRYPOINT ["/start"]
