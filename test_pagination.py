"""Tests for pagination module."""
import pytest
from pagination import paginate


def test_evenly_divisible_edge_case():
    """Regression test for #12: evenly divisible items must not produce an extra empty page."""
    items = list(range(10))
    result = paginate(items, page_size=5)
    assert len(result) == 2
    assert result[0] == [0, 1, 2, 3, 4]
    assert result[1] == [5, 6, 7, 8, 9]
    assert all(len(page) > 0 for page in result)


def test_evenly_divisible_single_page():
    """Regression test for #12: items exactly equal to page_size should produce one page."""
    result = paginate([1, 2, 3], page_size=3)
    assert len(result) == 1
    assert result[0] == [1, 2, 3]


def test_non_evenly_divisible():
    """Test non-evenly divisible case: 11 items with page_size=5 should return 3 pages."""
    items = list(range(11))
    result = paginate(items, page_size=5)
    assert len(result) == 3
    assert result[0] == [0, 1, 2, 3, 4]
    assert result[1] == [5, 6, 7, 8, 9]
    assert result[2] == [10]


def test_empty_items():
    """Test empty items should return empty list."""
    result = paginate([], page_size=5)
    assert result == []


def test_items_fewer_than_page_size():
    """Test when items are fewer than page_size."""
    items = [1, 2, 3]
    result = paginate(items, page_size=5)
    assert len(result) == 1
    assert result[0] == [1, 2, 3]


def test_page_size_one():
    """Test page size of 1."""
    items = [1, 2, 3]
    result = paginate(items, page_size=1)
    assert len(result) == 3
    assert result[0] == [1]
    assert result[1] == [2]
    assert result[2] == [3]


def test_invalid_page_size():
    """Test invalid page sizes."""
    items = [1, 2, 3]
    with pytest.raises(ValueError, match="Page size must be greater than 0"):
        paginate(items, page_size=0)
    with pytest.raises(ValueError, match="Page size must be greater than 0"):
        paginate(items, page_size=-1)


def test_various_types():
    """Test pagination works with various sequence types."""
    # Test with string
    result = paginate("abcdef", page_size=2)
    assert result == [['a', 'b'], ['c', 'd'], ['e', 'f']]
    
    # Test with tuple
    result = paginate((1, 2, 3, 4, 5), page_size=3)
    assert result == [[1, 2, 3], [4, 5]]