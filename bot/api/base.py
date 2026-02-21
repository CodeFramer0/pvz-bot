import logging

import aiohttp
from aiohttp import FormData

logger = logging.getLogger("BaseAPI")

class APIError(Exception):
    def __init__(self, status: int, detail: dict | str | None = None):
        self.status = status
        self.detail = detail
        super().__init__(f"APIError {status}: {detail}")

class BaseAPI:
    BASE_URL = "http://web:8000/api/v1/"

    _session: aiohttp.ClientSession | None = None

    def __init__(self, endpoint: str, jwt_client):
        self.endpoint = self.BASE_URL + endpoint
        self.jwt_client = jwt_client

    @classmethod
    async def get_session(cls) -> aiohttp.ClientSession:
        if cls._session is None or cls._session.closed:
            timeout = aiohttp.ClientTimeout(total=30)
            cls._session = aiohttp.ClientSession(timeout=timeout)
        return cls._session

    async def _headers(self):
        try:
            token = await self.jwt_client.get_access()
        except Exception:
            await self.jwt_client._login()
            token = await self.jwt_client.get_access()

        return {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    @staticmethod
    async def _process_response(response: aiohttp.ClientResponse) -> dict | list | None:
        try:
            data = await response.json()
        except Exception:
            data = await response.text()  # на случай не-JSON ответа

        if response.status >= 400:
            # Логируем для себя
            logger.error(f"API error: {response.status}, detail={data}")
            # Бросаем исключение наружу
            raise APIError(status=response.status, detail=data)

        # Если список с одним элементом — отдаём элемент
        if isinstance(data, list) and len(data) == 1:
            return data[0]
        return data

    def _build_url(self, path: str = "", id: int | None = None) -> str:
        if id is not None:
            return f"{self.endpoint}{id}/"
        if path:
            return f"{self.endpoint}{path}"
        return self.endpoint

    async def get(self, params=None, id: int | None = None, path: str = ""):
        url = self._build_url(path=path, id=id)
        session = await self.get_session()
        async with session.get(
            url, params=params, headers=await self._headers()
        ) as resp:
            return await self._process_response(resp)

    async def post(self, path: str = "", json: dict | None = None):
        url = self._build_url(path=path)
        session = await self.get_session()
        async with session.post(url, json=json, headers=await self._headers()) as resp:
            return await self._process_response(resp)

    async def put(self, id: int, json: dict | None = None):
        url = self._build_url(id=id)
        session = await self.get_session()
        async with session.put(url, json=json, headers=await self._headers()) as resp:
            return await self._process_response(resp)

    async def patch(self, id: int, json: dict | None = None):
        url = self._build_url(id=id)
        session = await self.get_session()
        async with session.patch(url, json=json, headers=await self._headers()) as resp:
            return await self._process_response(resp)

    async def delete(self, id: int):
        url = self._build_url(id=id)
        session = await self.get_session()
        async with session.delete(url, headers=await self._headers()) as resp:
            return await self._process_response(resp)

    async def post_multipart(
        self, path: str = "", json: dict | None = None, files: dict | None = None
    ):
        url = self._build_url(path=path)
        session = await self.get_session()
        headers = await self._headers()
        headers.pop("Content-Type", None)

        form = FormData()

        if json:
            for k, v in json.items():
                form.add_field(k, str(v))

        if files:
            for name, file in files.items():
                form.add_field(
                    name,
                    file,
                    filename=getattr(file, "name", "file.jpg"),
                    content_type="image/jpeg",
                )

        async with session.post(url, data=form, headers=headers) as resp:
            return await self._process_response(resp)

    @classmethod
    async def close_session(cls):
        if cls._session and not cls._session.closed:
            await cls._session.close()
