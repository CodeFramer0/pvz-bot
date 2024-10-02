import logging

import aiohttp
from loader import API_TOKEN, API_URL

HEADERS = {
    "Authorization": f"token {API_TOKEN}",
    "Accept": "application/json",
}


class BaseAPI:
    """Base API"""

    def __init__(self, endpoint):
        self.api_url = f"{API_URL}{endpoint}/"

    async def _process_response(self, response):
        """_summary_

        Args:
            response (_type_): _description_

        Returns:
            _type_: _description_
        """
        try:
            data = await response.json()
            response.raise_for_status()
            if not data:
                return None
            if isinstance(data, list):
                data = data if len(data) > 1 else data[0] if data else None
            return data
        except (aiohttp.ClientError, ValueError) as e:
            logging.error(f"An error occurred during response processing: {e}")
            logging.error(f"Response status: {response.status}")
            logging.error(f"Response content: {await response.text()}")
            return None

    async def create(self, body=None):
        """_summary_

        Args:
            body (_type_, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    self.api_url, json=body, headers=HEADERS
                ) as resp:
                    return await self._process_response(resp)
            except aiohttp.ClientError as e:
                logging.error(
                    f"An error occurred during POST request to {self.api_url}: {e}"
                )
                return None

    async def get(self, id=None, params=None):
        """_summary_

        Args:
            id (_type_, optional): _description_. Defaults to None.
            params (_type_, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        url = f"{self.api_url}{id}/" if id else self.api_url
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, params=params, headers=HEADERS) as resp:
                    return await self._process_response(resp)
            except aiohttp.ClientError as e:
                logging.error(f"An error occurred during GET request to {url}: {e}")
                return None

    async def update(self, id, body=None):
        """_summary_

        Args:
            id (_type_): _description_
            body (_type_, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        url = f"{self.api_url}{id}/"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.put(url, json=body, headers=HEADERS) as resp:
                    return await self._process_response(resp)
            except aiohttp.ClientError as e:
                logging.error(f"An error occurred during PUT request to {url}: {e}")
                return None

    async def delete(self, id):
        """_summary_

        Args:
            id (_type_): _description_

        Returns:
            _type_: _description_
        """
        url = f"{self.api_url}{id}/"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.delete(url, headers=HEADERS) as resp:
                    await self._process_response(resp)
                    return resp.status == 204
            except aiohttp.ClientError as e:
                logging.error(f"An error occurred during DELETE request to {url}: {e}")
                return None


class TelegramUserAPI(BaseAPI):
    """_summary_

    Args:
        BaseAPI (_type_): _description_
    """

    def __init__(self):
        super().__init__("telegram_users")


class OrderAPI(BaseAPI):
    """_summary_

    Args:
        BaseAPI (_type_): _description_
    """

    def __init__(self):
        super().__init__("orders")

    async def create(self, body=None, files=None):
        """_summary_

        Args:
            body (_type_, optional): _description_. Defaults to None.
            files (_type_, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        async with aiohttp.ClientSession() as session:
            try:
                form_data = aiohttp.FormData()

                if body:
                    for key, value in body.items():
                        form_data.add_field(key, str(value))

                if files:
                    for file_key, file_value in files.items():
                        form_data.add_field(
                            file_key,
                            file_value,
                            filename=file_value.name,
                            content_type="multipart/form-data",
                        )

                async with session.post(
                    self.api_url, data=form_data, headers=HEADERS
                ) as resp:
                    return await self._process_response(resp)
            except aiohttp.ClientError as e:
                logging.error(
                    f"An error occurred during POST request to {self.api_url}: {e}"
                )
                return None


class PickupPointAPI(BaseAPI):
    """_summary_"""

    def __init__(self):
        super().__init__("pickup_points")
