"""Pagination helper module."""
from typing import List, Any


def paginate(items: List[Any], page_size: int) -> List[List[Any]]:
    """Paginate items into pages of specified size."""
    if not items or page_size <= 0:
        return []
    
    pages = []
    total_pages = (len(items) + page_size - 1) // page_size
    
    for page_num in range(total_pages):
        start = page_num * page_size
        end = start + page_size
        pages.append(list(items[start:end]))
    
    return pages