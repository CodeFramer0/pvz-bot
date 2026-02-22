#!/bin/sh
set -e

# Утилита для ожидания доступности порта (БД)
wait_for_db() {
  echo "Waiting for database..."
  # Используем python-скрипт, так как nc/pg_isready может не быть в образе
  python << END
import socket
import time
import os
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while True:
    try:
        s.connect(('pvz-db', 5432))
        break
    except socket.error:
        time.sleep(1)
END
  echo "Database is up!"
}

wait_for_db

# --- БЛОК БЕСШОВНЫХ МИГРАЦИЙ ---
# На проде makemigrations НЕ НУЖНЫ. Только migrate.
# Если запускается несколько контейнеров, мигрирует только первый.
if [ "$SKIP_MIGRATIONS" != "true" ]; then
    echo "Applying migrations..."
    # Обычный migrate без создания новых файлов на лету
    poetry run python manage.py migrate --noinput
fi

echo "Collecting static files..."
# Сборка статики в MinIO/S3
poetry run python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
# Настройки для высокой нагрузки и бесшовности
exec poetry run gunicorn core.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 5 \
  --threads 5 \
  --worker-class gthread \
  --timeout 120 \
  --max-requests 1200 \
  --max-requests-jitter 100 \
  --access-logfile - \
  --error-log -