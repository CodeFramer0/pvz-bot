"""
robot/schemas/telegram_users.py

OpenAPI schemas для TelegramUser endpoints
"""

from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema

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

# ============= UPDATE SCHEMA =============
telegram_users_update_schema = extend_schema(
    summary="Обновить Telegram пользователя",
    description="Обновление данных Telegram пользователя (PUT — полностью, PATCH — частично)",
    tags=["TelegramUsers"],
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "nick_name": {"type": "string"},
                "is_blocked": {"type": "boolean"},
                "is_administrator": {"type": "boolean"},
            },
            "example": {
                "name": "John Doe",
                "nick_name": "johnny",
                "is_blocked": False,
                "is_administrator": True,
            },
        }
    },
    responses={
        200: OpenApiResponse(
            description="TelegramUser успешно обновлен",
            examples=[
                OpenApiExample(
                    "Success",
                    value={
                        "id": 1,
                        "user_id": 12345678,
                        "name": "John Doe",
                        "nick_name": "johnny",
                        "is_blocked": False,
                        "is_administrator": True,
                    },
                )
            ],
        ),
        400: OpenApiResponse(
            description="Ошибка валидации",
            examples=[
                OpenApiExample(
                    "Validation error",
                    value={"nick_name": ["Максимальная длина 32 символа"]},
                )
            ],
        ),
    },
)

# ============= BIND USER SCHEMA =============
telegram_users_bind_user_schema = extend_schema(
    summary="Привязать Telegram пользователя к AppUser",
    description=(
        "Создаёт AppUser по email/телефону, генерирует пароль и "
        "привязывает его к TelegramUser."
    ),
    tags=["TelegramUsers"],
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "email": {"type": "string", "format": "email"},
                "phone_number": {"type": "string"},
            },
            "required": ["email"],
        }
    },
    responses={
        200: OpenApiResponse(
            description="AppUser успешно создан и привязан",
            examples=[
                OpenApiExample(
                    "Success",
                    value={
                        "id": 12,
                        "email": "user@example.com",
                        "password": "A9f2KxPqL0sD",
                    },
                )
            ],
        ),
        400: OpenApiResponse(
            description="Ошибка валидации",
            examples=[
                OpenApiExample(
                    "Email required",
                    value={"email": "Обязательное поле"},
                )
            ],
        ),
    },
)

# ============= DELETE SCHEMA =============
telegram_users_destroy_schema = extend_schema(
    summary="Удалить Telegram пользователя",
    description="Удаляет Telegram пользователя по ID",
    tags=["TelegramUsers"],
    responses={
        204: OpenApiResponse(
            description="Telegram пользователь успешно удалён",
            examples=[
                OpenApiExample(
                    "Success",
                    value=None,
                )
            ],
        ),
        404: OpenApiResponse(
            description="Пользователь не найден",
            examples=[
                OpenApiExample(
                    "Not found",
                    value={"detail": "Not found."},
                )
            ],
        ),
    },
)
