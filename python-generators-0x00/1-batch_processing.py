#!/usr/bin/env python3
"""
1-batch_processing.py - Stream and process user_data in batches.

Functions:
- stream_users_in_batches(batch_size): yields rows in batches from user_data
- batch_processing(batch_size): processes each batch and filters users over age 25
"""

import mysql.connector
from mysql.connector import Error


def stream_users_in_batches(batch_size):
    """
    Generator that fetches rows from user_data table in batches.
    Yields lists of rows (each row is a dict).
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",       # change if needed
            password="root",   # change if needed
            database="ALX_prodev"
        )

        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT user_id, name, email, age FROM user_data;")

        while True:
            rows = cursor.fetchmany(batch_size)
            if not rows:
                break
            yield rows

        cursor.close()
        connection.close()

    except Error as e:
        print(f"Error streaming users in batches: {e}")
        return


def batch_processing(batc_

