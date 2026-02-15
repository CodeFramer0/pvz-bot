"""
robot/schemas/users.py

OpenAPI schemas для user endpoints
"""

from drf_spectacular.utils import extend_schema

# ============= LIST SCHEMA =============

users_list_schema = extend_schema(
    summary="Список пользователей",
    description="Получить список пользователей с фильтрацией и поиском",
    tags=["Users"],
)

# ============= CREATE SCHEMA =============

users_create_schema = extend_schema(
    summary="Регистрация",
    description="Зарегистрировать нового пользователя",
    tags=["Users"],
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "username": {"type": "string"},
                "email": {"type": "string", "format": "email"},
                "password": {"type": "string"},
                "password_confirm": {"type": "string"},
                "first_name": {"type": "string"},
                "last_name": {"type": "string"},
            },
            "required": ["username", "email", "password", "password_confirm"],
            "example": {
                "username": "john_doe",
                "email": "john@example.com",
                "password": "password123",
                "password_confirm": "password123",
                "first_name": "John",
                "last_name": "Doe",
            },
        }
    },
    responses={
        201: {
            "type": "object",
            "example": {
                "id": 1,
                "username": "john_doe",
                "email": "john@example.com",
                "first_name": "John",
                "last_name": "Doe",
            },
        }
    },
)

# ============= RETRIEVE SCHEMA =============

users_retrieve_schema = extend_schema(
    summary="Получить пользователя",
    description="Получить информацию о пользователе",
    tags=["Users"],
)

# ============= UPDATE SCHEMA =============

users_update_schema = extend_schema(
    summary="Обновить пользователя",
    description="Обновить информацию о пользователе",
    tags=["Users"],
)

# ============= DESTROY SCHEMA =============

users_destroy_schema = extend_schema(
    summary="Удалить пользователя",
    description="Удалить аккаунт пользователя",
    tags=["Users"],
)
