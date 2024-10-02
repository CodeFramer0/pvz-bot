FROM python:3.11

ARG SECRET_KEY
ARG DEBUG
ARG BOT_TOKEN
ARG BOT_NAME

ENV BOT_TOKEN=${BOT_TOKEN}
ENV BOT_NAME=${BOT_NAME}
ENV SECRET_KEY=${SECRET_KEY}
ENV DEBUG=${DEBUG}


WORKDIR /backend

COPY ./requirements.txt ./


RUN pip install --no-cache-dir -r requirements.txt
  


COPY . .
# ENTRYPOINT ["sh", "entrypoint.sh"]

EXPOSE 8000