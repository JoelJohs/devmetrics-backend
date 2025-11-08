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
async def test_ping(async_client: AsyncClient):
    response = await async_client.get("/api/ping")
    assert response.status_code == 200
    assert response.json() == {"ping": "pong"}
