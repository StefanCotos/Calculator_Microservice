from app.core.redis_cache import redis_client as default_redis_client
from app.core.logging_config import setup_logger
logger = setup_logger(__name__)


class MathService:
    def __init__(self, redis_instance=None):
        self.redis = redis_instance or default_redis_client

    async def fibonacci(self, n: int) -> int:
        """
        Calculates the n-th Fibonacci number.
        Args:
            n (int): The position in the Fibonacci sequence
                (must be ≥ 0).
        Returns:
            int: The n-th Fibonacci number.
        Raises:
            ValueError: If n is negative.
        """

        key = f"fib:{n}"
        cached = await self.redis.get(key)
        if cached:
            logger.debug(f"Cache hit for Fibonacci number at position {n}")
            return int(cached)

        if n < 0:
            logger.error("Fibonacci calculation failed: n must be >= 0")
            raise ValueError("n must be ≥ 0")
        if n in (0, 1):
            result = n
        else:
            result = await self.fibonacci(n - 1) + await self.fibonacci(n - 2)

        logger.debug(f"Calculated Fibonacci number at position {n}: {result}")

        await self.redis.set(key, result, ex=3600)
        return result

    async def factorial(self, n: int) -> int:
        """
        Calculates the factorial of a non-negative integer n.
        Args:
            n (int): The number for which to compute the factorial.
                Must be ≥ 0.
        Returns:
            int: The factorial of n.
        Raises:
            ValueError: If n is negative.
        """

        key = f"fact:{n}"
        cached = await self.redis.get(key)
        if cached:
            logger.debug(f"Cache hit for factorial of {n}")
            return int(cached)

        if n < 0:
            logger.error("Factorial calculation failed: n must be >= 0")
            raise ValueError("n must be ≥ 0")
        result = 1
        for i in range(2, n + 1):
            result *= i

        logger.debug(f"Calculated factorial of {n}: {result}")

        await self.redis.set(key, result, ex=3600)
        return result

    async def power(self, x: float, y: float) -> float:
        """
        Calculates the result of raising x to the power of y.
        Args:
            x (float): The base number.
            y (float): The exponent.
        Returns:
            float: The result of x raised to the power of y.
        """

        key = f"pow:{x}:{y}"
        cached = await self.redis.get(key)
        if cached:
            logger.debug(f"Cache hit for power calculation: {x} ^ {y}")
            return float(cached)

        result = x ** y

        logger.debug(f"Calculated power: {x} ^ {y} = {result}")

        await self.redis.set(key, result, ex=3600)
        return result
