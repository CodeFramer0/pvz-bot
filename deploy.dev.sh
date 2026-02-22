#!/bin/bash
set -e

echo "🚀 Начинаем бесшовный деплой..."

# 1. Собираем свежие образы
docker compose build web bot celery-worker

# 2. Запускаем вторую копию web (теперь их 2)
# --no-deps чтобы не перезапускать БД и Редис
echo "📥 Запуск новой версии Django (web=2)..."
docker compose up -d --no-deps --scale web=2 web

# 3. Ждем, пока новый контейнер станет Healthy
echo "⏳ Ожидание проверки здоровья (Healthcheck)..."
MAX_RETRIES=12
COUNT=0

while [ $COUNT -lt $MAX_RETRIES ]; do
  # Проверяем, сколько контейнеров 'web' имеют статус healthy
  HEALTHY_COUNT=$(docker ps --filter "name=pvz-django" --filter "health=healthy" -q | wc -l)
  
  if [ "$HEALTHY_COUNT" -eq "2" ]; then
    echo "✅ Новая версия готова к работе!"
    break
  fi
  
  echo "...ждем (попытка $((COUNT+1))/$MAX_RETRIES)"
  sleep 5
  COUNT=$((COUNT+1))
done

if [ "$COUNT" -eq "$MAX_RETRIES" ]; then
  echo "❌ Ошибка: Новая версия не прошла Healthcheck. Откат..."
  docker compose up -d --scale web=1 web
  exit 1
fi

# 4. Схлопываем до 1 контейнера (Docker удалит самый старый)
echo "♻️ Удаление старой версии (web=1)..."
docker compose up -d --scale web=1 web

# 5. Перезапуск фоновых сервисов
echo "🤖 Перезапуск бота и воркеров..."
docker compose restart bot celery-worker celery-beat

echo "✨ Деплой успешно завершен!"
