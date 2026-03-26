"""Tests for calculator module."""
import pytest
from decimal import Decimal
from calculator import add, subtract, multiply, divide


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


# Bool rejection tests (3 tests)
def test_add_rejects_bool():
    with pytest.raises(TypeError):
        add(True, 1)


def test_subtract_rejects_bool():
    with pytest.raises(TypeError):
        subtract(False, 1)


def test_multiply_rejects_bool():
    with pytest.raises(TypeError):
        multiply(True, False)


# Decimal rejection tests (3 tests)
def test_add_rejects_decimal():
    with pytest.raises(TypeError):
        add(Decimal('1'), 2)


def test_subtract_rejects_decimal():
    with pytest.raises(TypeError):
        subtract(1, Decimal('2'))


def test_divide_rejects_decimal():
    with pytest.raises(TypeError):
        divide(Decimal('10'), Decimal('2'))


# Complex rejection tests (3 tests)
def test_add_rejects_complex():
    with pytest.raises(TypeError):
        add(1+2j, 3)


def test_multiply_rejects_complex():
    with pytest.raises(TypeError):
        multiply(2, 3+4j)


def test_divide_rejects_complex():
    with pytest.raises(TypeError):
        divide(1+0j, 1)


# String coercion tests (3 tests)
def test_add_string_coercion():
    assert add('2', '3') == 5.0


def test_subtract_string_coercion():
    assert subtract('10.5', '0.5') == 10.0


def test_multiply_rejects_nonnumeric_string():
    with pytest.raises(TypeError):
        multiply('hello', 2)
