"""
AeroFlight Suite
Flight Deletion Queries

Database-level operations responsible for deleting
flight records and their dependent V5 runway-performance data.
"""

import sqlite3

from .common import get_connection
from .queries import DELETE_FLIGHT, DELETE_RUNWAY_PERFORMANCE


def delete_flight_database(flight_number):
    """
    Delete a flight by flight number as one atomic database operation.

    Version 5
    ---------
    A flight may have a dependent record in
    ``flight_runway_performance``. Both records must be deleted
    in the same SQLite transaction so the database can never be
    left in a partially deleted state.

    Parameters
    ----------
    flight_number : str
        Flight number to delete.

    Returns
    -------
    int
        Number of flight rows deleted.

    Raises
    ------
    ValueError
        If the flight number is missing.
    RuntimeError
        If SQLite reports a database error. The transaction is
        rolled back automatically when an exception occurs.
    """

    if flight_number is None:
        raise ValueError("Flight number is required.")

    normalized_flight_number = str(flight_number).strip()

    if not normalized_flight_number:
        raise ValueError("Flight number is required.")

    try:
        # IMPORTANT:
        # Keep both DELETE statements on the SAME connection.
        # The connection context manager commits when the block
        # exits successfully and rolls back when an exception is
        # raised. This makes the deletion atomic.
        with get_connection() as connection:
            cursor = connection.cursor()

            # --------------------------------------------------
            # 1. Delete dependent V5 runway-performance data.
            # --------------------------------------------------
            cursor.execute(
                DELETE_RUNWAY_PERFORMANCE,
                (normalized_flight_number,),
            )

            # --------------------------------------------------
            # 2. Delete the primary flight record.
            # --------------------------------------------------
            cursor.execute(
                DELETE_FLIGHT,
                (normalized_flight_number,),
            )

            # Return the number of deleted flights, not the number
            # of deleted dependent performance records.
            return cursor.rowcount

    except sqlite3.Error as error:
        raise RuntimeError(
            f"Database error while deleting flight "
            f"'{normalized_flight_number}': {error}"
        ) from error
