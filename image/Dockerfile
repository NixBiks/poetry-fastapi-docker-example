ARG PYTHON_TAG=3.11.1-bullseye
ARG POETRY_VERSION=1.3.2

# Create base image
FROM python:${PYTHON_TAG} as base
LABEL maintainer="Nicolai Bjerre Pedersen <mr.bjerre@gmail.com>"

    # https://docs.python.org/3/using/cmdline.html#envvar-PYTHONUNBUFFERED
ENV PYTHONUNBUFFERED=1 \
    # https://docs.python.org/3/using/cmdline.html#envvar-PYTHONDONTWRITEBYTECODE
    PYTHONDONTWRITEBYTECODE=1


# Create builder image
FROM base as builder

ENV PYTHONPATH=/application_root \
    # https://python-poetry.org/docs/configuration/#virtualenvsin-project
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_HOME=/opt/poetry
ENV VENV_PATH="${PYTHONPATH}/.venv" \
    PATH="${POETRY_HOME}/bin:${PATH}"

# set working directory
WORKDIR ${PYTHONPATH}

# install poetry
COPY image/install.python-poetry.org /tmp/install.python-poetry.org
RUN POETRY_VERSION="${POETRY_VERSION}" python /tmp/install.python-poetry.org


# Create runtime image
FROM builder as build

# install dependencies
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root

# copy project
COPY playground playground
COPY tests tests
COPY Makefile README.md ./

# install project
RUN poetry install

# run tests
RUN make test && \
    make lint

# remove test dependencies
RUN poetry install --only main --sync

# Create runtime image
FROM base as runtime
WORKDIR /usr/src/app
ENV PATH="/application_root/.venv/bin:${PATH}" \
    APP_MODULE="playground.main:app" \
    GUNICORN_CONF="gunicorn_conf.py"
COPY image/gunicorn_conf.py image/start.sh ./
COPY --from=build /application_root/.venv /application_root/.venv
COPY --from=build /application_root/playground /usr/src/app/playground
CMD ["./start.sh"]
