class MathService:
    def fibonacci(self, n: int) -> int:
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
        if n < 0:
            raise ValueError("n trebuie să fie ≥ 0")
        a, b = 0, 1
        for _ in range(n):
            a, b = b, a + b
        return a

    def factorial(self, n: int) -> int:
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

        if n < 0:
            raise ValueError("n trebuie să fie ≥ 0")
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result

    def power(self, x: float, y: float) -> float:
        """
        Calculates the result of raising x to the power of y.
        Args:
            x (float): The base number.
            y (float): The exponent.
        Returns:
            float: The result of x raised to the power of y.
        """
        return x ** y
