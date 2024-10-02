FROM python:3.11

WORKDIR /bot

# Установка аргументов
ARG BOT_TOKEN
ARG BOT_NAME
ARG API_URL
ARG API_TOKEN

# Установка переменных окружения
ENV BOT_TOKEN=${BOT_TOKEN}
ENV BOT_NAME=${BOT_NAME}
ENV API_URL=${API_URL}
ENV API_TOKEN=${BACKEND_API_TOKEN}

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

