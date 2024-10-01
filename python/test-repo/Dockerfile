# Base Image
FROM python:3.10.13-slim-bookworm as python-base

ENV \
    APP_PATH="/app" \
    PIP_DISABLED_PIP_VERSION_CHECK=1 \
    POETRY_VERSION=1.8.3 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=false

# Builder Image
FROM python-base as build

WORKDIR $APP_PATH

COPY pyproject.toml ./

RUN pip3 install poetry==$POETRY_VERSION \
    && poetry export --without-hashes --without dev -f requirements.txt -o requirements.txt

# Final Image
FROM python-base as final

WORKDIR $APP_PATH

COPY --from=build $APP_PATH/requirements.txt ./

RUN pip3 install --upgrade pip \
    && pip3 install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

#CMD ["python3", "main.py"]