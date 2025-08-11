import pytest
import pytest_asyncio
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport
from app.main import app


class DummyRedis:
    def __init__(self):
        self.store = {}

    async def get(self, key):
        return self.store.get(key)

    async def set(self, key, value, ex=None):
        self.store[key] = value


@pytest_asyncio.fixture
async def client(monkeypatch):
    monkeypatch.setattr("app.services.math_service.MathService.__init__", lambda self,
                        redis_instance=None: setattr(self, "redis", DummyRedis()))
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_factorial_success(client):
    response = await client.post("/api/factorial", json={"n": 5})
    assert response.status_code == 200
    assert response.json()["result"] == 120


@pytest.mark.asyncio
async def test_factorial_invalid(client):
    response = await client.post("/api/factorial", json={"n": -1})
    assert response.status_code in (400, 422)

# @pytest.mark.asyncio
# async def test_fibonacci_success(client):
#     response = await client.post("/api/fibonacci", json={"n": 6})
#     assert response.status_code == 200
#     assert response.json()["result"] == 8

# @pytest.mark.asyncio
# async def test_pow_success(client):
#     response = await client.post("/api/pow", json={"x": 2, "y": 3})
#     assert response.status_code == 200
#     assert response.json()["result"] == 8
