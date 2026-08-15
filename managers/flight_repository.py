"""
AeroFlight Suite
Flight Repository

Persistence gateway for Flight-related operations.

Version 5.0

The repository is the persistence boundary between
application managers and the database layer.

V5 adds Runway Performance integration while keeping
all V4 flight operations backward compatible.

Architecture
------------
Core / Managers
        ↓
Flight Repository
        ↓
Database Manager
        ↓
SQLite

Runway Performance
        ↓
Runway Repository
        ↓
Database Manager
        ↓
SQLite
"""

from database.common import get_connection

from database.database_manager import (
    flight_exists as db_flight_exists,
    insert_flight as db_insert_flight,
    delete_flight_database as db_delete_flight,
    update_status as db_update_status,
    update_weather as db_update_weather,
    update_flight_cost as db_update_flight_cost,
    update_distance as db_update_distance,
    search_flights as db_search_flights,
    advanced_search as db_advanced_search,
    filter_flights as db_filter_flights,
    sort_flights as db_sort_flights,
    get_all_flights as db_get_all_flights,
    get_statistics as db_get_statistics,
    backup_database as db_backup_database,
    save_runway_performance as db_save_runway_performance,
)

# ============================================================
# PUBLIC API
# ============================================================

__all__ = (
    "exists",
    "save",
    "delete",
    "update_status",
    "update_weather",
    "update_flight_cost",
    "update_distance",
    "get_all",
    "get_statistics",
    "search",
    "advanced_search",
    "filter_by",
    "sort_by",
    "backup",
)


# ============================================================
# INTERNAL NORMALIZATION HELPERS
# ============================================================


def _rows_to_dicts(rows):
    """
    Convert database result rows into dictionaries.
    """

    if not rows:
        return []

    normalized_rows = []

    for row in rows:

        if isinstance(row, dict):
            normalized_rows.append(dict(row))

        else:
            normalized_rows.append(dict(row))

    return normalized_rows


def _row_to_dict(row):
    """
    Convert a single database row into a dictionary.
    """

    if row is None:
        return None

    if isinstance(row, dict):
        return dict(row)

    return dict(row)


# ============================================================
# EXISTENCE
# ============================================================


def exists(flight_number):
    """
    Check whether a flight number already exists.
    """

    if not isinstance(flight_number, str):
        return False

    normalized_flight_number = flight_number.strip().upper()

    if not normalized_flight_number:
        return False

    return db_flight_exists(
        normalized_flight_number,
    )


# ============================================================
# CREATE
# ============================================================


def save(flight):
    """
    Persist a complete Flight domain object atomically.

    Version 5
    ---------
    The Flight row and its optional runway-performance row are
    written through the same SQLite connection. If either write
    fails, the complete operation is rolled back.
    """

    if flight is None:
        raise ValueError("Flight object cannot be None.")

    weather = flight.weather_data()

    runway = getattr(flight, "runway", None)
    runway_performance = getattr(flight, "runway_performance", None)

    with get_connection() as connection:
        flight_id = db_insert_flight(
            connection=connection,
            flight_number=flight.flight_number,
            flight_date=flight.flight_date,
            pilot=flight.pilot,
            manufacturer=flight.manufacturer,
            model=flight.model,
            departure_code=flight.departure_code,
            departure_city=flight.departure_city,
            arrival_code=flight.arrival_code,
            arrival_city=flight.arrival_city,
            distance=flight.distance,
            speed=flight.speed,
            fuel_price=flight.fuel_price,
            flight_time=flight.flight_time,
            fuel_needed=flight.fuel_needed,
            fuel_cost=flight.fuel_cost,
            status=flight.status,
            wind_speed=weather.get("wind_speed", 0),
            wind_direction=weather.get("wind_direction", ""),
            temperature=weather.get("temperature", 0),
            pressure=weather.get("pressure", 0),
            humidity=weather.get("humidity", 0),
            visibility=weather.get("visibility", 0),
            weather_condition=weather.get("condition", ""),
            weather_severity=weather.get("severity", ""),
            weather_factor=flight.weather_factor,
        )

        if runway is not None and runway_performance:
            db_save_runway_performance(
                flight_number=str(flight.flight_number).strip(),
                airport_code=str(runway.airport_code).strip().upper(),
                runway_id=str(runway.runway_id).strip().upper(),
                required_takeoff_distance=runway_performance[
                    "required_takeoff_distance"
                ],
                required_landing_distance=runway_performance[
                    "required_landing_distance"
                ],
                takeoff_margin=runway_performance["takeoff_margin"],
                landing_margin=runway_performance["landing_margin"],
                takeoff_status=runway_performance["takeoff_status"],
                landing_status=runway_performance["landing_status"],
                temperature=runway_performance.get(
                    "temperature",
                    weather.get("temperature", 15.0),
                ),
                aircraft_weight=runway_performance.get("aircraft_weight"),
                reference_weight=runway_performance.get("reference_weight"),
                connection=connection,
            )

        return flight_id


# ============================================================
# DELETE
# ============================================================


def delete(flight_number):
    """
    Delete a flight by flight number.

    Performance deletion is handled by the database
    relationship defined in V5.
    """

    if not flight_number:
        raise ValueError("Flight number is required.")

    return db_delete_flight(
        str(flight_number).strip(),
    )


# ============================================================
# UPDATE STATUS
# ============================================================


def update_status(
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

    return db_update_status(
        str(flight_number).strip(),
        str(status).strip(),
    )


# ============================================================
# UPDATE WEATHER
# ============================================================


def update_weather(
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

    return db_update_weather(
        str(flight_number).strip(),
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


# ============================================================
# UPDATE FUEL COST
# ============================================================


def update_flight_cost(
    flight_number,
    fuel_cost,
):
    """
    Update fuel cost.
    """

    if not flight_number:
        raise ValueError("Flight number is required.")

    return db_update_flight_cost(
        str(flight_number).strip(),
        fuel_cost,
    )


# ============================================================
# UPDATE DISTANCE
# ============================================================


def update_distance(
    flight_number,
    distance,
):
    """
    Update flight distance.
    """

    if not flight_number:
        raise ValueError("Flight number is required.")

    return db_update_distance(
        str(flight_number).strip(),
        distance,
    )


# ============================================================
# READ — ALL FLIGHTS
# ============================================================


def get_all():
    """
    Return all stored flights as dictionaries.
    """

    rows = db_get_all_flights()

    return _rows_to_dicts(
        rows,
    )


# ============================================================
# READ — STATISTICS
# ============================================================


def get_statistics():
    """
    Return aggregate flight statistics.
    """

    row = db_get_statistics()

    statistics = _row_to_dict(
        row,
    )

    if statistics is None:
        return {
            "total_flights": 0,
            "total_distance": 0,
            "total_flight_time": 0,
            "total_fuel": 0,
            "total_cost": 0,
        }

    return {
        "total_flights": statistics.get(
            "total_flights",
            0,
        )
        or 0,
        "total_distance": statistics.get(
            "total_distance",
            0,
        )
        or 0,
        "total_flight_time": statistics.get(
            "total_flight_time",
            0,
        )
        or 0,
        "total_fuel": statistics.get(
            "total_fuel",
            0,
        )
        or 0,
        "total_cost": statistics.get(
            "total_cost",
            0,
        )
        or 0,
    }


# ============================================================
# GLOBAL SEARCH
# ============================================================


def search(keyword):
    """
    Search flights using a global keyword.
    """

    rows = db_search_flights(
        keyword,
    )

    return _rows_to_dicts(
        rows,
    )


# ============================================================
# ADVANCED SEARCH
# ============================================================


def advanced_search(
    flight_number=None,
    aircraft=None,
    departure=None,
    arrival=None,
):
    """
    Perform an advanced flight search.
    """

    rows = db_advanced_search(
        flight_number=flight_number or "",
        aircraft=aircraft or "",
        departure=departure or "",
        arrival=arrival or "",
    )

    return _rows_to_dicts(
        rows,
    )


# ============================================================
# FILTER
# ============================================================


def filter_by(
    field,
    value,
):
    """
    Filter flights.
    """

    rows = db_filter_flights(
        field,
        value,
    )

    return _rows_to_dicts(
        rows,
    )


# ============================================================
# SORT
# ============================================================


def sort_by(sort_type):
    """
    Sort flights.
    """

    rows = db_sort_flights(
        sort_type,
    )

    return _rows_to_dicts(
        rows,
    )


# ============================================================
# BACKUP
# ============================================================


def backup():
    """
    Create a database backup.
    """

    return db_backup_database()
