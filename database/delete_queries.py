"""
AeroFlight Suite
Flight Deletion Queries

Database-level operations responsible for deleting
flight records.
"""

from .common import execute_query

from .queries import DELETE_FLIGHT


def delete_flight_database(flight_number):
    """
    Delete a flight by flight number.

    Parameters
    ----------
    flight_number : str
        Flight number to delete.

    Returns
    -------
    int
        Number of affected rows.
    """

    if not flight_number:
        raise ValueError("Flight number is required.")

    return execute_query(
        DELETE_FLIGHT,
        (str(flight_number).strip(),),
    )
