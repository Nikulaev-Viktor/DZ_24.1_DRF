# Используем базовый образ Python
FROM python:3.12-slim

# Устанавливаем Poetry
RUN pip install --no-cache-dir poetry

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы Poetry
COPY pyproject.toml poetry.lock .

# Устанавливаем зависимости
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-dev

# Копируем код приложения
COPY . .