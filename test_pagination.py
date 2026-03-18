"""Tests for pagination module."""
from pagination import paginate


def test_basic_pagination():
    """Test basic pagination with uneven division."""
    result = paginate(list(range(7)), 3)
    assert result == [[0, 1, 2], [3, 4, 5], [6]]
    assert len(result) == 3


def test_exact_division_edge_case():
    """Regression test for off-by-one bug with exact division."""
    result = paginate(list(range(10)), 5)
    assert result == [[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]
    assert len(result) == 2  # Should be exactly 2 pages, not 3


def test_empty_input():
    """Test pagination with empty input."""
    result = paginate([], 5)
    assert result == []


def test_single_page():
    """Test when all items fit in a single page."""
    result = paginate(list(range(3)), 5)
    assert result == [[0, 1, 2]]
    assert len(result) == 1


def test_single_item():
    """Test pagination with a single item."""
    result = paginate([42], 5)
    assert result == [[42]]
    assert len(result) == 1


def test_page_size_one():
    """Test with page size of 1."""
    result = paginate(list(range(3)), 1)
    assert result == [[0], [1], [2]]
    assert len(result) == 3


def test_zero_page_size():
    """Test with zero page size."""
    result = paginate(list(range(5)), 0)
    assert result == []


def test_negative_page_size():
    """Test with negative page size."""
    result = paginate(list(range(5)), -1)
    assert result == []