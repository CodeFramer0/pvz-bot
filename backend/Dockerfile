FROM python:3.11-slim AS dev

ENV POETRY_VERSION=1.8.2
WORKDIR /backend

# Системные зависимости для сборки всех пакетов (dev + prod)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libffi-dev \
    python3-dev \
    curl \
    postgresql-client \
    netcat-openbsd \
    git \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && ln -s /root/.local/bin/poetry /usr/local/bin/poetry \
    && poetry config virtualenvs.create false \
    && apt-get clean

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-interaction --no-ansi  # устанавливаем и dev-зависимости

COPY . .
CMD ["pytest", "--maxfail=1", "--disable-warnings", "-q"]
