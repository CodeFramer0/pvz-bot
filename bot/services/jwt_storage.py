# services/jwt_storage.py
from redis import Redis

redis = Redis(host="redis", port=6379, db=5, decode_responses=True)


def save_tokens(tg_id, access, refresh=None):
    redis.hset(
        f"jwt:{tg_id}",
        mapping={
            "access": str(access),
            "refresh": str(refresh) if refresh is not None else "",
        },
    )


def get_access_token(tg_id: int) -> str | None:
    return redis.hget(f"jwt:{tg_id}", "access")


def get_refresh_token(tg_id: int) -> str | None:
    return redis.hget(f"jwt:{tg_id}", "refresh")
