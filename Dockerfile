FROM python:3.8-slim

# environment variables
ARG DJANGO_ENV=develop \
    PORT=8000

ENV DJANGO_ENV=$DJANGO_ENV \
    PORT=$PORT \
    PROJECT_DIR="/code" \
    # python
    PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    # pip
    PIP_NO_CHACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # poetry
    POETRY_VERSION=1.1.7 \
    POETRY_VIRTUALENVS_CREATE=false \
    PATH="${PATH}:/root/.poetry/bin"

# system dependencies
RUN apt-get update && apt-get upgrade -y \
    && apt-get install --no-install-recommends --no-install-suggests -y \
    build-essential \
    libpq-dev \
    postgresql \
    postgresql-contrib \
    python3-dev \
    && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/* \
    && pip install poetry==$POETRY_VERSION && poetry --version

# set working directory
WORKDIR $PROJECT_DIR

# copy script as an entry point:
COPY ./scripts ${PROJECT_DIR}/scripts/

# copy dependencies only
COPY ./pyproject.toml ./poetry.lock ${PROJECT_DIR}/

# setting up proper permissions
RUN chmod +x ${PROJECT_DIR}/scripts/entrypoint.sh \
    && chmod +x ${PROJECT_DIR}/scripts/start_api.sh \
    && chmod +x ${PROJECT_DIR}/scripts/start_worker.sh \
    && groupadd -r api && useradd -d /code -r -g api api \
    && chown api:api -R /code \
    # install dependencies
    && poetry config virtualenvs.create false \
    && poetry install $(test $DJANGO_ENV = production && echo "--no-dev") --no-interaction --no-ansi

# expose port
EXPOSE $PORT

# copy project
COPY --chown=api:api . ${PROJECT_DIR}/

# running as non-root user:
USER api

# run server
CMD ./scripts/entrypoint.sh
