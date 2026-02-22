# services/jwt_storage.py
from redis import Redis

# Убедись, что хост 'redis' доступен из контейнера бота
redis = Redis(host="redis", port=6379, db=5, decode_responses=True)

def save_bot_tokens(access, refresh):
    redis.hset(
        "bot_system_auth",
        mapping={
            "access": str(access),
            "refresh": str(refresh),
        },
    )

def get_bot_tokens():
    return redis.hgetall("bot_system_auth") # Вернет словарь {'access': '...', 'refresh': '...'}
