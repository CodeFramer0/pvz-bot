"""
robot/schemas/pickup_points.py

OpenAPI schemas для pickup_point endpoints
"""
from drf_spectacular.utils import extend_schema

# ============= LIST SCHEMA =============

pickup_points_list_schema = extend_schema(
    summary="Список пунктов выдачи",
    description="Получить список всех пунктов выдачи с фильтрацией по маркетплейсу и поиском по адресу",
    tags=["PickupPoints"],
)

# ============= CREATE SCHEMA =============

pickup_points_create_schema = extend_schema(
    summary="Создать пункт выдачи",
    description="Создать новый пункт выдачи",
    tags=["PickupPoints"],
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "address": {"type": "string"},
                "marketplace": {
                    "type": "string",
                    "enum": ["ozon", "wb", "yandex", "cdek", "mail"]
                },
                "admin_telegram_user_id": {"type": "integer"},
            },
            "required": ["address", "marketplace", "admin_telegram_user_id"],
            "example": {
                "address": "ул. Пушкина, д. 10",
                "marketplace": "ozon",
                "admin_telegram_user_id": 1
            }
        }
    },
    responses={
        201: {
            "type": "object",
            "example": {
                "id": 1,
                "address": "ул. Пушкина, д. 10",
                "marketplace": "ozon"
            }
        }
    }
)

# ============= RETRIEVE SCHEMA =============

pickup_points_retrieve_schema = extend_schema(
    summary="Получить пункт выдачи",
    description="Получить информацию о пункте выдачи",
    tags=["PickupPoints"],
)

# ============= UPDATE SCHEMA =============

pickup_points_update_schema = extend_schema(
    summary="Обновить пункт выдачи",
    description="Обновить данные пункта выдачи",
    tags=["PickupPoints"],
)

# ============= DESTROY SCHEMA =============

pickup_points_destroy_schema = extend_schema(
    summary="Удалить пункт выдачи",
    description="Удалить пункт выдачи",
    tags=["PickupPoints"],
)

# ============= BY MARKETPLACE SCHEMA =============

pickup_points_by_marketplace_schema = extend_schema(
    summary="Пункты по маркетплейсу",
    description="Получить пункты выдачи определенного маркетплейса",
    tags=["PickupPoints"],
    parameters=[{
        'name': 'marketplace',
        'in': 'query',
        'description': 'ozon, wb, yandex, cdek, mail',
        'schema': {'type': 'string'},
        'required': True
    }]
)
