"""Simple calculator module."""
from decimal import Decimal


def _sanitize(value):
    """Sanitize and validate input value."""
    if isinstance(value, bool):
        raise TypeError(f"Input type 'bool' is not supported")
    if isinstance(value, complex):
        raise TypeError(f"Input type 'complex' is not supported")
    if isinstance(value, Decimal):
        raise TypeError(f"Input type 'Decimal' is not supported")
    if isinstance(value, str):
        try:
            return float(value)
        except ValueError:
            raise TypeError(f"Cannot convert string '{value}' to number")
    if isinstance(value, (int, float)):
        return value
    raise TypeError(f"Input type '{type(value).__name__}' is not supported")


def add(a: float, b: float) -> float:
    """Add two numbers."""
    a = _sanitize(a)
    b = _sanitize(b)
    return a + b


def subtract(a: float, b: float) -> float:
    """Subtract b from a."""
    a = _sanitize(a)
    b = _sanitize(b)
    return a - b


def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    a = _sanitize(a)
    b = _sanitize(b)
    return a * b


def divide(a: float, b: float) -> float:
    """Divide a by b."""
    a = _sanitize(a)
    b = _sanitize(b)
    return a / b
