from .base import BaseAPI


class TelegramUserAPI(BaseAPI):
    def __init__(self, jwt_client):
        super().__init__("telegram-users/", jwt_client)


class PickupPointAPI(BaseAPI):
    def __init__(self, jwt_client):
        super().__init__("pickup-points/", jwt_client)


class OrderAPI(BaseAPI):
    def __init__(self, jwt_client):
        super().__init__("orders/", jwt_client)
