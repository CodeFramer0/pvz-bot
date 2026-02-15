"""
robot/schemas/orders.py

OpenAPI schemas для order endpoints
"""

from drf_spectacular.utils import extend_schema

# ============= LIST SCHEMA =============

orders_list_schema = extend_schema(
    summary="Список заказов",
    description="Получить список всех заказов текущего пользователя с фильтрацией и поиском",
    tags=["Orders"],
)

# ============= CREATE SCHEMA =============

orders_create_schema = extend_schema(
    summary="Создать заказ",
    description="Создать новый заказ в пункте выдачи",
    tags=["Orders"],
    request={
        "multipart/form-data": {
            "type": "object",
            "properties": {
                "full_name": {"type": "string"},
                "amount": {"type": "string"},
                "comment": {"type": "string"},
                "barcode_image": {"type": "string", "format": "binary"},
                "pickup_point_id": {"type": "integer"},
            },
            "required": ["full_name", "amount", "barcode_image", "pickup_point_id"],
        }
    },
    responses={
        201: {
            "type": "object",
            "example": {
                "id": 1,
                "full_name": "John Doe",
                "amount": "1500",
                "status": "pending",
                "date_created": "2024-01-15T10:30:00Z",
            },
        }
    },
)

# ============= RETRIEVE SCHEMA =============

orders_retrieve_schema = extend_schema(
    summary="Получить заказ",
    description="Получить подробную информацию о заказе",
    tags=["Orders"],
)

# ============= UPDATE SCHEMA =============

orders_update_schema = extend_schema(
    summary="Обновить заказ",
    description="Обновить данные заказа (только владелец)",
    tags=["Orders"],
)

# ============= DESTROY SCHEMA =============

orders_destroy_schema = extend_schema(
    summary="Удалить заказ",
    description="Удалить заказ (только владелец)",
    tags=["Orders"],
)

# ============= UPDATE STATUS SCHEMA =============

orders_update_status_schema = extend_schema(
    summary="Обновить статус заказа",
    description="Изменить статус заказа (pending, completed, processing, etc.)",
    tags=["Orders"],
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "status": {
                    "type": "string",
                    "enum": [
                        "pending",
                        "completed",
                        "barcode_expired",
                        "not_arrived_goods",
                        "insufficient_funds",
                        "card_not_linked",
                        "contact_manager",
                        "processed",
                        "arrived",
                    ],
                },
            },
            "required": ["status"],
            "example": {"status": "completed"},
        }
    },
)
