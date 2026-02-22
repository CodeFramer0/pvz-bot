#!/bin/sh
set -e

echo "Applying migrations..."
poetry run python manage.py migrate --noinput

echo "Collecting static files..."
poetry run python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
# Исправлено: --access-logfile вместо --access-log
exec poetry run gunicorn core.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 4 \
  --threads 4 \
  --worker-class gthread \
  --timeout 120 \
  --access-logfile - \
  --error-log -
