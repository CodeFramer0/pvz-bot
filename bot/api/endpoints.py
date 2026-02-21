from .base import BaseAPI


class AuthAPI(BaseAPI):
    def __init__(self, jwt_client):
        super().__init__("auth/", jwt_client)

    async def send_verification_code(self, email: str) -> dict | None:
        return await self.post(path="verify/send-code/", json={"email": email})

    async def verify_code(self, email: str, code: str) -> dict | None:
        return await self.post(
            path="verify/confirm/", json={"email": email, "code": code}
        )


class UsersAPI(BaseAPI):
    def __init__(self, jwt_client):
        super().__init__("users/", jwt_client)


class TelegramUserAPI(BaseAPI):
    def __init__(self, jwt_client):
        super().__init__("telegram-users/", jwt_client)

    async def bind_user(
        self, id: int, email: str, phone_number: str | None = None
    ) -> dict | None:
        payload = {"email": email}
        if phone_number:
            payload["phone_number"] = phone_number

        return await self.post(path=f"{id}/bind_user/", json=payload)


class PickupPointAPI(BaseAPI):
    def __init__(self, jwt_client):
        super().__init__("pickup-points/", jwt_client)


class OrderAPI(BaseAPI):
    def __init__(self, jwt_client):
        super().__init__("orders/", jwt_client)


class MarketplaceAPI(BaseAPI):
    def __init__(self, jwt_client):
        super().__init__("marketplaces/", jwt_client)
