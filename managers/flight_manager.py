"""
AeroFlight Suite
Flight Manager

Application-level manager for flight operations.

Architecture
------------

core
    ↓
flight_manager
    ↓
flight_repository
    ↓
database_manager
    ↓
SQLite

Responsibilities
----------------
Flight Manager:
    - application-level validation
    - application-level operation boundary
    - delegation to repository

Flight Repository:
    - persistence
    - database result normalization
    - SQLite boundary

Database:
    - SQL execution
    - schema
    - transactions
"""

from managers.flight_repository import (
    exists as repository_exists,
    save as repository_save,
)

# ============================================================
# FLIGHT EXISTENCE
# ============================================================


def flight_exists(flight_number):
    """
    Check whether a flight already exists.

    This function belongs to the application manager layer.
    Database access is delegated to the repository.

    Parameters
    ----------
    flight_number : str
        Flight number to check.

    Returns
    -------
    bool
        True if the flight exists, otherwise False.
    """

    if flight_number is None:
        return False

    if not isinstance(
        flight_number,
        str,
    ):
        return False

    normalized_flight_number = flight_number.strip().upper()

    if not normalized_flight_number:
        return False

    return repository_exists(
        normalized_flight_number,
    )


# ============================================================
# CREATE FLIGHT
# ============================================================


def create_flight(flight):
    """
    Create and persist a complete Flight object.

    The manager does not perform SQL operations.

    Persistence is delegated to the repository.

    Parameters
    ----------
    flight : Flight
        Complete Flight domain object.

    Returns
    -------
    int
        Database ID of the newly created flight.

    Raises
    ------
    ValueError
        If the Flight object is missing.
    """

    if flight is None:
        raise ValueError("Flight object cannot be None.")

    return repository_save(
        flight,
    )


# ============================================================
# PUBLIC API
# ============================================================


__all__ = (
    "flight_exists",
    "create_flight",
)
