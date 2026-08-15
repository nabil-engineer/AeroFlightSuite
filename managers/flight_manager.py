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
    delete as repository_delete,
    update_status as repository_update_status,
    update_weather as repository_update_weather,
    update_flight_cost as repository_update_flight_cost,
    update_distance as repository_update_distance,
    get_all as repository_get_all,
    get_statistics as repository_get_statistics,
    search as repository_search,
    advanced_search as repository_advanced_search,
    filter_by as repository_filter_by,
    sort_by as repository_sort_by,
    backup as repository_backup,
)

# ==========================================================
# FLIGHT EXISTENCE
# ==========================================================


def flight_exists(flight_number):
    """
    Check whether a flight already exists.
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


# ==========================================================
# CREATE FLIGHT
# ==========================================================


def create_flight(flight):
    """
    Create and persist a complete Flight object.
    """

    if flight is None:
        raise ValueError("Flight object cannot be None.")

    return repository_save(
        flight,
    )


# ==========================================================
# DELETE FLIGHT
# ==========================================================


def delete_flight(flight_number):
    """
    Delete a flight by flight number.
    """

    if not flight_number:
        raise ValueError("Flight number is required.")

    normalized_flight_number = str(flight_number).strip().upper()

    if not normalized_flight_number:
        raise ValueError("Flight number is required.")

    return repository_delete(
        normalized_flight_number,
    )


# ==========================================================
# UPDATE STATUS
# ==========================================================


def update_flight_status(
    flight_number,
    status,
):
    """
    Update the status of a flight.
    """

    if not flight_number:
        raise ValueError("Flight number is required.")

    if not status or not str(status).strip():
        raise ValueError("Flight status is required.")

    return repository_update_status(
        str(flight_number).strip().upper(),
        str(status).strip(),
    )


# ==========================================================
# UPDATE WEATHER
# ==========================================================


def update_flight_weather(
    flight_number,
    weather_factor,
    wind_speed,
    wind_direction,
    temperature,
    pressure,
    humidity,
    visibility,
    weather_condition,
    weather_severity,
):
    """
    Update complete weather information.
    """

    if not flight_number:
        raise ValueError("Flight number is required.")

    return repository_update_weather(
        str(flight_number).strip().upper(),
        weather_factor,
        wind_speed,
        wind_direction,
        temperature,
        pressure,
        humidity,
        visibility,
        weather_condition,
        weather_severity,
    )


# ==========================================================
# UPDATE FUEL COST
# ==========================================================


def update_flight_cost(
    flight_number,
    fuel_cost,
):
    """
    Update the fuel cost of a flight.
    """

    if not flight_number:
        raise ValueError("Flight number is required.")

    return repository_update_flight_cost(
        str(flight_number).strip().upper(),
        fuel_cost,
    )


# ==========================================================
# UPDATE DISTANCE
# ==========================================================


def update_flight_distance(
    flight_number,
    distance,
):
    """
    Update the distance of a flight.
    """

    if not flight_number:
        raise ValueError("Flight number is required.")

    return repository_update_distance(
        str(flight_number).strip().upper(),
        distance,
    )


# ==========================================================
# GET ALL FLIGHTS
# ==========================================================


def get_all_flights():
    """
    Return all flights.
    """

    return repository_get_all()


# ==========================================================
# STATISTICS
# ==========================================================


def get_flight_statistics():
    """
    Return aggregate flight statistics.
    """

    return repository_get_statistics()


# ==========================================================
# GLOBAL SEARCH
# ==========================================================


def search_flights(keyword):
    """
    Search flights using a global keyword.
    """

    return repository_search(
        keyword,
    )


# ==========================================================
# ADVANCED SEARCH
# ==========================================================


def advanced_search_flights(
    flight_number=None,
    aircraft=None,
    departure=None,
    arrival=None,
):
    """
    Perform an advanced flight search.
    """

    return repository_advanced_search(
        flight_number=flight_number,
        aircraft=aircraft,
        departure=departure,
        arrival=arrival,
    )


# ==========================================================
# FILTER
# ==========================================================


def filter_flights(
    field,
    value,
):
    """
    Filter flights by field.
    """

    return repository_filter_by(
        field,
        value,
    )


# ==========================================================
# SORT
# ==========================================================


def sort_flights(sort_type):
    """
    Sort flights using the repository.
    """

    return repository_sort_by(
        sort_type,
    )


# ==========================================================
# BACKUP
# ==========================================================


def backup_database():
    """
    Create a database backup.
    """

    return repository_backup()


# ==========================================================
# PUBLIC API
# ==========================================================

__all__ = (
    "flight_exists",
    "create_flight",
    "delete_flight",
    "update_flight_status",
    "update_flight_weather",
    "update_flight_cost",
    "update_flight_distance",
    "get_all_flights",
    "get_flight_statistics",
    "search_flights",
    "advanced_search_flights",
    "filter_flights",
    "sort_flights",
    "backup_database",
)
