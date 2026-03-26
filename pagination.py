"""Pagination helper module."""

from typing import List, Sequence, TypeVar

T = TypeVar('T')


def paginate(items: Sequence[T], page_size: int) -> List[List[T]]:
    """Paginate a sequence of items into pages of specified size."""
    if page_size <= 0:
        raise ValueError("Page size must be greater than 0")
    
    if not items:
        return []
    
    pages = []
    for i in range(0, len(items), page_size):
        pages.append(list(items[i:i + page_size]))
    
    return pages