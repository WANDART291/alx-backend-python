#!/usr/bin/env python3
"""
0-stream_users.py - Stream rows from the user_data table using a generator.

Prototype:
    def stream_users()

This function connects to the ALX_prodev database and streams
rows from the user_data table one by one using yield.
"""

import mysql.connector
from mysql.connector import Error


def stream_users():
    """Generator that fetches rows one by one from user_data table."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",       # change if needed
            password="root",   # change if needed
            database="ALX_prodev"
        )

        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT user_id, name, email, age FROM user_data;")

        for row in cursor:
            yield row

        cursor.close()
        connection.close()

    except Error as e:
        print(f"Error streaming users: {e}")
        return

