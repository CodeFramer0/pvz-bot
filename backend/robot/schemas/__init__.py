"""
robot/schemas/__init__.py

Импортирует все OpenAPI schemas из отдельных модулей
"""
from .auth import (
    email_login_schema,
    username_login_schema,
    refresh_token_schema,
    logout_schema,
    current_user_schema,
    change_password_schema,
    verify_token_schema,
)

from .orders import (
    orders_list_schema,
    orders_create_schema,
    orders_retrieve_schema,
    orders_update_schema,
    orders_destroy_schema,
    orders_update_status_schema,
)

from .pickup_points import (
    pickup_points_list_schema,
    pickup_points_create_schema,
    pickup_points_retrieve_schema,
    pickup_points_update_schema,
    pickup_points_destroy_schema,
    pickup_points_by_marketplace_schema,
)

from .users import (
    users_list_schema,
    users_create_schema,
    users_retrieve_schema,
    users_update_schema,
    users_destroy_schema,
)

from .telegram_users import (
    telegram_users_list_schema,
    telegram_users_retrieve_schema,
)

__all__ = [
    # Auth Schemas
    'email_login_schema',
    'username_login_schema',
    'refresh_token_schema',
    'logout_schema',
    'current_user_schema',
    'change_password_schema',
    'verify_token_schema',
    
    # Order Schemas
    'orders_list_schema',
    'orders_create_schema',
    'orders_retrieve_schema',
    'orders_update_schema',
    'orders_destroy_schema',
    'orders_update_status_schema',
    
    # PickupPoint Schemas
    'pickup_points_list_schema',
    'pickup_points_create_schema',
    'pickup_points_retrieve_schema',
    'pickup_points_update_schema',
    'pickup_points_destroy_schema',
    'pickup_points_by_marketplace_schema',
    
    # User Schemas
    'users_list_schema',
    'users_create_schema',
    'users_retrieve_schema',
    'users_update_schema',
    'users_destroy_schema',
    
    # TelegramUser Schemas
    'telegram_users_list_schema',
    'telegram_users_retrieve_schema',
]
