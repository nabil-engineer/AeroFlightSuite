import sqlite3
from config.config import DATABASE_FILE


def get_connection():
    """
    Return SQLite connection.
    """
    connection = sqlite3.connect(DATABASE_FILE)
    connection.row_factory = sqlite3.Row
    return connection


def execute_query(query, parameters=(), fetch=False):
    """
    Execute SQL query.
    """
    with get_connection() as connection:

        cursor = connection.cursor()

        cursor.execute(query, parameters)

        if fetch:
            return cursor.fetchall()

        return cursor.rowcount


def execute_single(query, parameters=()):
    """
    Execute SQL query and return one row.
    """
    with get_connection() as connection:

        cursor = connection.cursor()

        cursor.execute(query, parameters)

        return cursor.fetchone()
