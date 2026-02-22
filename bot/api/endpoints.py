from .base import BaseAPI

class AuthAPI(BaseAPI):
    def __init__(self, jwt_client):
        # На бэкенде путь /api/v1/auth/
        super().__init__("auth", jwt_client)

    async def send_reset_code(self, email: str) -> dict | None:
        """Отправить код для сброса пароля (Redis flow)"""
        return await self.post(path="password-reset/send-code/", json={"email": email})

    async def reset_password_confirm(self, email: str, temp_token: str, password: str) -> dict | None:
        """Финальный сброс пароля"""
        return await self.post(
            path="password-reset/confirm/", 
            json={
                "email": email, 
                "code": temp_token, 
                "new_password": password,
                "new_password_confirm": password
            }
        )

    async def send_verification_code(self, email: str) -> dict | None:
        return await self.post(path="password-reset/send-code/", json={"email": email})

    async def verify_code(self, email: str, code: str) -> dict | None:
        # На бэкенде мы используем путь подтверждения кода для сброса
        return await self.post(path="password-reset/verify-code/", json={"email": email, "code": code})

class UsersAPI(BaseAPI):
    def __init__(self, jwt_client):
        super().__init__("users", jwt_client)

    async def get_me(self):
        """Получить инфо о боте (системном юзере)"""
        return await self.get(path="me/")

class TelegramUserAPI(BaseAPI):
    def __init__(self, jwt_client):
        super().__init__("telegram-users", jwt_client)

    async def bind_user(self, tg_record_id: int, email: str) -> dict | None:
        """Привязать ТГ-аккаунт к системному пользователю"""
        # На бэкенде путь: /api/v1/telegram-users/{id}/bind-user/
        return await self.post(path=f"{tg_record_id}/bind-user/", json={"email": email})

class OrderAPI(BaseAPI):
    def __init__(self, jwt_client):
        super().__init__("orders", jwt_client)

    async def get_my_orders(self):
        return await self.get(path="my-orders/")

    async def update_status(self, order_id: int, new_status: str):
        """Смена статуса заказа через PATCH"""
        return await self.patch(id=order_id, json={"status": new_status})

class PickupPointAPI(BaseAPI):
    def __init__(self, jwt_client):
        super().__init__("pickup-points", jwt_client)

    async def get_by_marketplace(self, marketplace_id: int):
        """Фильтрация ПВЗ по маркетплейсу"""
        return await self.get(path="by-marketplace/", params={"marketplace": marketplace_id})

class MarketplaceAPI(BaseAPI):
    def __init__(self, jwt_client):
        super().__init__("marketplaces", jwt_client)
