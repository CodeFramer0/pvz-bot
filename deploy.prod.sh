#!/bin/bash

# Цвета для вывода
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
RED='\033[0;31m'
GRAY='\033[0;90m'
NC='\033[0m' # No Color

echo -e "${CYAN}🚀 Начинаем бесшовный деплой (PROD)...${NC}"

COMPOSE_FILE="docker-compose.prod.yml"
SERVICE_NAME="web"

# 1. Собираем свежий образ
echo -e "${YELLOW}📦 Сборка нового образа...${NC}"
docker compose -f $COMPOSE_FILE build $SERVICE_NAME

# 2. Запускаем вторую копию (старая + новая работают вместе)
echo -e "${YELLOW}🆙 Запуск новой версии (scaling up to 2)...${NC}"
docker compose -f $COMPOSE_FILE up -d --no-deps --scale $SERVICE_NAME=2 $SERVICE_NAME

# 3. Ждем, пока НОВЫЙ контейнер пройдет Healthcheck
echo -ne "${GRAY}⏳ Ожидание прогрева нового контейнера...${NC}"
MAX_RETRIES=20
COUNT=0
IS_HEALTHY=false

while [ $COUNT -lt $MAX_RETRIES ]; do
    # Считаем только контейнеры со статусом 'healthy' для конкретного сервиса
    HEALTHY_COUNT=$(docker ps --filter "label=com.docker.compose.service=$SERVICE_NAME" --filter "health=healthy" -q | wc -l)
    
    if [ "$HEALTHY_COUNT" -ge 2 ]; then
        IS_HEALTHY=true
        break
    fi
    
    echo -n "."
    sleep 3
    COUNT=$((COUNT + 1))
done

if [ "$IS_HEALTHY" = false ]; then
    echo -e "\n${RED}❌ Ошибка: Новая версия не прошла Healthcheck! Откат к 1 копии...${NC}"
    docker compose -f $COMPOSE_FILE up -d --scale $SERVICE_NAME=1 $SERVICE_NAME
    exit 1
fi

echo -e "\n${GREEN}✅ Новая версия готова и принимает трафик!${NC}"

# 4. Удаляем старую версию (Docker прибьет самый старый контейнер)
echo -e "${YELLOW}♻️ Удаление старой версии (scaling down to 1)...${NC}"
docker compose -f $COMPOSE_FILE up -d --scale $SERVICE_NAME=1 $SERVICE_NAME

# 5. Рестарт зависимых сервисов
echo -e "${CYAN}🤖 Обновление бота и воркеров...${NC}"
docker compose -f $COMPOSE_FILE restart bot celery-worker celery-beat

# 6. Очистка мусора
echo -e "${GRAY}🧹 Очистка старых образов...${NC}"
docker image prune -f

echo -e "${GREEN}✨ Деплой завершен успешно!${NC}"
