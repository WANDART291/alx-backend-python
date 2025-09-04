#!/usr/bin/env python3
"""
seed.py - Setup and populate the ALX_prodev MySQL database.

Functions:
- connect_db() : connects to the MySQL server
- create_database(connection) : creates the ALX_prodev database if it does not exist
- connect_to_prodev() : connects to the ALX_prodev database
- create_table(connection) : creates the user_data table if it does not exist
- insert_data(connection, csv_file) : inserts data from a CSV file into the table
"""

import mysql.connector
from mysql.connector import Error
import csv
import uuid


def connect_db():
    """Connect to the MySQL server (without specifying a database)."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",       # change if you use a different MySQL user
            password="root"    # change if you have a different MySQL password
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
    return None


def create_database(connection):
    """Create ALX_prodev database if it does not exist."""
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
        cursor.close()
    except Error as e:
        print(f"Error creating database: {e}")


def connect_to_prodev():
    """Connect to the ALX_prodev database."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",       # change if needed
            password="root",   # change if needed
            database="ALX_prodev"
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error while connecting to ALX_prodev: {e}")
    return None


def create_table(connection):
    """Create user_data table if it does not exist."""
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id CHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL NOT NULL,
                INDEX (user_id)
            );
        """)
        connection.commit()
        cursor.close()
        print("Table user_data created successfully")
    except Error as e:
        print(f"Error creating table: {e}")


def insert_data(connection, csv_file):
    """Insert data from a CSV file into the user_data table."""
    try:
        cursor = connection.cursor()

        with open(csv_file, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                user_id = str(uuid.uuid4())  # generate unique UUID
                name = row["name"]
                email = row["email"]
                age = row["age"]

                # Insert only if email not already in database
                cursor.execute(
                    "SELECT COUNT(*) FROM user_data WHERE email = %s",
                    (email,)
                )
                if cursor.fetchone()[0] == 0:
                    cursor.execute(
                        "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)",
                        (user_id, name, email, age)
                    )

        connection.commit()
        cursor.close()
    except Error as e:
        print(f"Error inserting data: {e}")
    except FileNotFoundError:
        print(f"CSV file '{csv_file}' not found.")

