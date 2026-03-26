"""Tests for calculator module."""
import pytest
from calculator import add, subtract, multiply, divide, square_root


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


def test_square_root():
    assert square_root(4) == 2.0
    assert square_root(0) == 0.0
    assert square_root(9) == 3.0
    with pytest.raises(ValueError):
        square_root(-1)
