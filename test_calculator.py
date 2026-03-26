"""Tests for calculator module."""
from calculator import add, subtract, multiply, divide, power


def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0


def test_subtract():
    assert subtract(5, 3) == 2
    assert subtract(0, 5) == -5


def test_multiply():
    assert multiply(3, 4) == 12
    assert multiply(0, 5) == 0


def test_divide():
    assert divide(10, 2) == 5.0
    assert divide(7, 2) == 3.5


def test_power():
    assert power(2, 3) == 8
    assert power(5, 0) == 1


def test_power_zero_base_negative_exp():
    try:
        power(0, -1)
        assert False, "Expected ValueError"
    except ValueError:
        pass
