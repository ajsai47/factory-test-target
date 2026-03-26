"""Simple calculator module."""


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


def power(base: float, exp: float) -> float:
    """Raise base to the power of exp."""
    if base == 0 and exp < 0:
        raise ValueError("Cannot raise zero to a negative power.")
    return base ** exp
