"""
robot/schemas/telegram_users.py

OpenAPI schemas для telegram_user endpoints
"""
from drf_spectacular.utils import extend_schema

# ============= LIST SCHEMA =============
telegram_users_list_schema = extend_schema(
    summary="Список Telegram пользователей",
    description="Получить список Telegram пользователей с фильтрацией и поиском",
    tags=["TelegramUsers"],
)

# ============= RETRIEVE SCHEMA =============
telegram_users_retrieve_schema = extend_schema(
    summary="Получить Telegram пользователя",
    description="Получить информацию о Telegram пользователе",
    tags=["TelegramUsers"],
)

# ============= CREATE SCHEMA =============
telegram_users_create_schema = extend_schema(
    summary="Создать Telegram пользователя",
    description="Создать нового пользователя (используется middleware при первом сообщении)",
    tags=["TelegramUsers"],
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "user_id": {"type": "integer"},
                "username": {"type": "string"},
                "first_name": {"type": "string"},
                "last_name": {"type": "string"},
            },
            "required": ["user_id"],
            "example": {
                "user_id": 12345678,
                "username": "john_doe",
                "first_name": "John",
                "last_name": "Doe",
            },
        }
    },
    responses={
        201: {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "user_id": {"type": "integer"},
                "username": {"type": "string"},
                "first_name": {"type": "string"},
                "last_name": {"type": "string"},
            },
            "example": {
                "id": 1,
                "user_id": 12345678,
                "username": "john_doe",
                "first_name": "John",
                "last_name": "Doe",
            },
        },
        400: {"type": "object", "example": {"user_id": ["This field is required."]}},
    },
)
