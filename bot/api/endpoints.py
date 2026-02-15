from .base import BaseAPI


class UsersAPI(BaseAPI):
    def __init__(self, jwt_client):
        super().__init__("users/", jwt_client)


class TelegramUserAPI(BaseAPI):
    def __init__(self, jwt_client):
        super().__init__("telegram-users/", jwt_client)

    async def bind_user(
        self, id: int, email: str, phone_number: str | None = None
    ) -> dict | None:
        """
        Привязать TelegramUser к AppUser через bind_user endpoint.
        Возвращает dict с id, email и password нового AppUser.
        """
        payload = {"email": email}
        if phone_number:
            payload["phone_number"] = phone_number

        return await self.post(f"{id}/bind_user/", json=payload)


class PickupPointAPI(BaseAPI):
    def __init__(self, jwt_client):
        super().__init__("pickup-points/", jwt_client)


class OrderAPI(BaseAPI):
    def __init__(self, jwt_client):
        super().__init__("orders/", jwt_client)
