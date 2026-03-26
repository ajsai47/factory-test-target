"""Simple calculator module."""
import math


def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b


def subtract(a: float, b: float) -> float:
    """Subtract b from a."""
    return a - b


def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b


def divide(a: float, b: float) -> float:
    """Divide a by b."""
    return a / b


def square_root(n: float) -> float:
    """Return the square root of n."""
    if n < 0:
        raise ValueError("Cannot compute square root of negative number")
    return math.sqrt(n)
