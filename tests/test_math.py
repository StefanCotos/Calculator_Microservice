import pytest
from app.services.math_service import MathService

class DummyRedis:
    def __init__(self):
        self.store = {}
    async def get(self, key):
        return self.store.get(key)
    async def set(self, key, value, ex=None):
        self.store[key] = value

@pytest.mark.asyncio
async def test_factorial():
    service = MathService(redis_instance=DummyRedis())
    assert await service.factorial(0) == 1
    assert await service.factorial(1) == 1
    assert await service.factorial(5) == 120
    with pytest.raises(ValueError):
        await service.factorial(-1)

@pytest.mark.asyncio
async def test_fibonacci():
    service = MathService(redis_instance=DummyRedis())
    assert await service.fibonacci(0) == 0
    assert await service.fibonacci(1) == 1
    assert await service.fibonacci(5) == 5
    with pytest.raises(ValueError):
        await service.fibonacci(-1)

@pytest.mark.asyncio
async def test_pow():
    service = MathService(redis_instance=DummyRedis())
    assert await service.power(2, 3) == 8
    assert await service.power(5, 0) == 1
    assert await service.power(9, 0.5) == 3
