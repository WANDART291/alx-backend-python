#!/usr/bin/env python3
"""
3-average_age.py - Compute average user age efficiently using a generator.

Functions:
- stream_user_ages(): yields user ages one by one from user_data
- compute_average_age(): consumes the generator and calculates the average
"""

import seed


def stream_user_ages():
    """
    Generator that streams user ages from the user_data table.
    Yields ages one by one as integers.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data;")

    for row in cursor:
        yield int(row["age"])

    cursor.close()
    connection.close()


def compute_average_age():
    """
    Computes and prints the average age of users
    without loading the entire dataset into memory.
    """
    total_age = 0
    count = 0

    for age in stream_user_ages():
        total_age += age
        count += 1

    if count == 0:
        print("Average age of users: 0")
    else:
        average = total_age / count
        print(f"Average age of users: {average:.2f}")


if __name__ == "__main__":
    compute_average_age()

