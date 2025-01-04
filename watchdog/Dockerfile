# Используем базовый образ
FROM alpine:latest

# Устанавливаем необходимые утилиты
RUN apk add --no-cache bash docker-cli

# Копируем скрипт в контейнер
COPY watchdog.sh /watchdog.sh

# Делаем скрипт исполняемым
RUN chmod +x /watchdog.sh

# Запускаем скрипт
CMD ["bash", "/watchdog.sh"]
