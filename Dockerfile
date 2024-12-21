FROM kalilinux/kali-rolling:latest

RUN apt update && apt install -y \
    python3-pip

RUN pip install poetry --break-system-packages

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app
COPY pyproject.toml poetry.lock ./
COPY README.md ./

RUN poetry install --without dev --no-root \
    && rm -rf $POETRY_CACHE_DIR

COPY nobu ./nobu
COPY notion-templates ./notion-templates
COPY .env ./

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

RUN poetry install --without dev

CMD ["nobu"]
