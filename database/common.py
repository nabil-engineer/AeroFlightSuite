"""
AeroFlight Suite
Database Common Utilities

Centralized SQLite connection and query execution helpers.

All database query modules use this module to ensure
consistent connection handling, transactions, and errors.
"""

import sqlite3

from config.config import DATABASE_FILE


def get_connection():
    """
    Create and return a configured SQLite connection.

    Returns
    -------
    sqlite3.Connection
        SQLite connection using Row objects.
    """

    connection = sqlite3.connect(
        DATABASE_FILE,
    )

    # SQLite disables foreign-key enforcement by default for each
    # new connection. AeroFlight Suite V5 relies on the declared
    # relationships between flights, runways, and runway performance,
    # so enforcement must be enabled on EVERY connection.
    connection.execute("PRAGMA foreign_keys = ON")

    connection.row_factory = sqlite3.Row

    return connection


def execute_query(
    query,
    parameters=(),
    fetch=False,
    fetch_one=False,
):
    """
    Execute a SQL statement using a managed database connection.

    Parameters
    ----------
    query : str
        SQL statement.

    parameters : tuple
        Parameters passed safely to the SQL statement.

    fetch : bool
        If True, return all matching rows.

    fetch_one : bool
        If True, return the first matching row.

    Returns
    -------
    list[sqlite3.Row] | sqlite3.Row | int | None
        Query results or affected row count.

    Raises
    ------
    ValueError
        If both fetch and fetch_one are requested.

    RuntimeError
        If a SQLite database error occurs.
    """

    if fetch and fetch_one:
        raise ValueError("fetch and fetch_one cannot both be True.")

    try:
        with get_connection() as connection:

            cursor = connection.cursor()

            cursor.execute(
                query,
                parameters,
            )

            if fetch_one:
                return cursor.fetchone()

            if fetch:
                return cursor.fetchall()

            connection.commit()

            return cursor.rowcount

    except sqlite3.Error as error:
        raise RuntimeError(f"Database error: {error}") from error


def execute_single(
    query,
    parameters=(),
):
    """
    Execute a SELECT query and return one row.

    This helper is kept as a dedicated convenience API
    for callers that explicitly need a single record.
    """

    return execute_query(
        query,
        parameters,
        fetch_one=True,
    )
