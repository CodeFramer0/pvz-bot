#!/bin/bash

# Интервал проверки (в секундах)
CHECK_INTERVAL=30

while true; do
  echo "Checking for unhealthy containers..."
  # Получаем список контейнеров с состоянием unhealthy
  for container in $(docker ps --filter "health=unhealthy" --format "{{.Names}}"); do
    echo "$(date): Restarting unhealthy container: $container"
    docker restart "$container"
  done
  sleep $CHECK_INTERVAL
done
