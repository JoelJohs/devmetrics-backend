import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from app.main import app


@pytest_asyncio.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.mark.asyncio
async def test_root(async_client: AsyncClient):
    response = await async_client.get("/")
    assert response.status_code == 200
    json = response.json()
    assert json["message"] == "Welcome to the DevMetrics API"
    assert json.get("ok") is True


@pytest.mark.asyncio
async def test_favicon_exists(async_client: AsyncClient): 
    response = await async_client.get("/favicon.ico")
    assert response.status_code == 200
