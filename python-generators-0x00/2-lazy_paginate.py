#!/usr/bin/env python3
"""
2-lazy_paginate.py - Simulate fetching paginated data lazily from user_data.

Functions:
- paginate_users(page_size, offset): fetches a page of users starting at given offset
- lazy_paginate(page_size): generator that yields pages of users on demand
"""

import seed


def paginate_users(page_size, offset):
    """
    Fetch a page of users from the database.
    Returns a list of user dictionaries (empty list if no more rows).
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows


def lazy_paginate(page_size):
    """
    Generator that lazily yields pages of users from user_data.
    Uses only one loop, fetching the next page when needed.
    """
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size

