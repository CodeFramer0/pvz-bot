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
        # Гарантируем слеш в конце базового пути: /api/v1/users/
        self.endpoint = f"{self.BASE_URL}{endpoint.strip('/')}/"
        self.jwt_client = jwt_client

    @classmethod
    async def get_session(cls) -> aiohttp.ClientSession:
        if cls._session is None or cls._session.closed:
            timeout = aiohttp.ClientTimeout(total=30)
            cls._session = aiohttp.ClientSession(timeout=timeout)
        return cls._session

    async def _headers(self, is_multipart=False):
        token = await self.jwt_client.get_access()
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
        }
        if not is_multipart:
            headers["Content-Type"] = "application/json"
        return headers

    @staticmethod
    async def _process_response(response: aiohttp.ClientResponse) -> dict | list | None:
        try:
            data = await response.json()
        except Exception:
            data = await response.text()

        if response.status >= 400:
            logger.error(f"API Error [{response.status}]: {data}")
            raise APIError(status=response.status, detail=data)
        return data

    def _build_url(self, path: str = "", id: int | None = None) -> str:
        url = self.endpoint
        if id is not None:
            url = f"{url}{id}/"
        if path:
            url = f"{url}{path.strip('/')}/"
        return url

    # === ОСНОВНЫЕ МЕТОДЫ ===

    async def get(self, params=None, id: int | None = None, path: str = ""):
        url = self._build_url(path=path, id=id)
        session = await self.get_session()
        async with session.get(url, params=params, headers=await self._headers()) as resp:
            return await self._process_response(resp)

    async def post(self, path: str = "", json: dict | None = None):
        url = self._build_url(path=path)
        session = await self.get_session()
        async with session.post(url, json=json, headers=await self._headers()) as resp:
            return await self._process_response(resp)

    async def patch(self, id: int, json: dict | None = None, path: str = ""):
        url = self._build_url(id=id, path=path)
        session = await self.get_session()
        async with session.patch(url, json=json, headers=await self._headers()) as resp:
            return await self._process_response(resp)

    async def put(self, id: int, json: dict | None = None, path: str = ""):
        url = self._build_url(id=id, path=path)
        session = await self.get_session()
        async with session.put(url, json=json, headers=await self._headers()) as resp:
            return await self._process_response(resp)

    async def delete(self, id: int, path: str = ""):
        url = self._build_url(id=id, path=path)
        session = await self.get_session()
        async with session.delete(url, headers=await self._headers()) as resp:
            return await self._process_response(resp)

    # === MULTIPART (Картинки) ===

    async def post_multipart(self, path: str = "", fields: dict | None = None, files: dict | None = None):
        url = self._build_url(path=path)
        session = await self.get_session()
        
        form = FormData()
        if fields:
            for k, v in fields.items():
                if v is not None:
                    form.add_field(k, str(v))

        if files:
            for name, file_bytes in files.items():
                form.add_field(
                    name,
                    file_bytes,
                    filename="file.jpg",
                    content_type="image/jpeg"
                )

        async with session.post(url, data=form, headers=await self._headers(is_multipart=True)) as resp:
            return await self._process_response(resp)

    @classmethod
    async def close_session(cls):
        if cls._session and not cls._session.closed:
            await cls._session.close()
