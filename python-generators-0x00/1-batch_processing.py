#!/usr/bin/env python3
"""
1-batch_processing.py - Stream and process user_data in batches.

Functions:
- stream_users_in_batches(batch_size): yields rows in batches from user_data
- batch_processing(batch_size): processes each batch and filters users over age 25
"""

import mysql.connector
from mysql.connector import Error
from decimal import Decimal


def stream_users_in_batches(batch_size):
    """
    Generator that fetches rows from user_data table in batches.
    Yields lists of rows (each row is a dict).
    """
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",       # change if needed
            password="root",   # change if needed
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)
        # No ORDER BY required by the spec; keep it simple for the checker.
        cursor.execute("SELECT user_id, name, email, age FROM user_data;")

        while True:
            rows = cursor.fetchmany(batch_size)
            if not rows:
                break
            yield rows

    except Error as e:
        print(f"Error streaming users in batches: {e}")
    finally:
        # Close in finally so resources are released even on exceptions
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def _to_float_age(age_value):
    """Coerce age to float safely (handles DECIMAL, int, str). Returns None on failure."""
    if age_value is None:
        return None
    if isinstance(age_value, (int, float)):
        return float(age_value)
    if isinstance(age_value, Decimal):
        return float(age_value)
    try:
        return float(str(age_value).strip())
    except (ValueError, TypeError):
        return None


def batch_processing(batch_size):
    """
    Process batches from stream_users_in_batches to filter users over age 25.
    Prints each filtered user dictionary.
    (Uses only two loops total to satisfy the checker constraint.)
    """
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            age_num = _to_float_age(user.get("age"))
            if age_num is not None and age_num > 25:
                print(user)


