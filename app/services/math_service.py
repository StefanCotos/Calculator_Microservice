class MathService:
    def fibonacci(self, n: int) -> int:
        if n < 0:
            raise ValueError("n trebuie să fie ≥ 0")
        a, b = 0, 1
        for _ in range(n):
            a, b = b, a + b
        return a

    def factorial(self, n: int) -> int:
        if n < 0:
            raise ValueError("n trebuie să fie ≥ 0")
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result

    def power(self, x: float, y: float) -> float:
        return x ** y
