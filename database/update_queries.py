"""
AeroFlight Suite
Flight Update Queries

Database-level operations responsible for updating
flight records.
"""

from .common import execute_query
from .queries import (
    UPDATE_STATUS,
    UPDATE_DISTANCE,
    UPDATE_FUEL_COST,
    UPDATE_WEATHER,
    UPSERT_RUNWAY_PERFORMANCE,
)


def update_status(
    flight_number,
    status,
):
    """
    Update the status of a flight.

    Parameters
    ----------
    flight_number : str
        Flight number to update.

    status : str
        New flight status.

    Returns
    -------
    int
        Number of affected rows.
    """

    if not flight_number:
        raise ValueError("Flight number is required.")

    if not status or not str(status).strip():
        raise ValueError("Flight status is required.")

    return execute_query(
        UPDATE_STATUS,
        (
            str(status).strip(),
            str(flight_number).strip(),
        ),
    )


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
    Update the complete weather information of a flight.

    Parameters
    ----------
    flight_number : str
        Flight number to update.

    weather_factor : float
        Weather impact factor.

    wind_speed : float
        Wind speed.

    wind_direction : str
        Wind direction.

    temperature : float
        Temperature.

    pressure : float
        Atmospheric pressure.

    humidity : float
        Humidity percentage.

    visibility : float
        Visibility distance.

    weather_condition : str
        Weather condition description.

    weather_severity : str
        Weather severity.

    Returns
    -------
    int
        Number of affected rows.
    """

    if not flight_number:
        raise ValueError("Flight number is required.")

    return execute_query(
        UPDATE_WEATHER,
        (
            weather_factor,
            wind_speed,
            wind_direction,
            temperature,
            pressure,
            humidity,
            visibility,
            weather_condition,
            weather_severity,
            str(flight_number).strip(),
        ),
    )


def update_flight_cost(
    flight_number,
    fuel_cost,
):
    """
    Update the fuel cost of a flight.

    Parameters
    ----------
    flight_number : str
        Flight number to update.

    fuel_cost : float
        New fuel cost.

    Returns
    -------
    int
        Number of affected rows.
    """

    if not flight_number:
        raise ValueError("Flight number is required.")

    return execute_query(
        UPDATE_FUEL_COST,
        (
            fuel_cost,
            str(flight_number).strip(),
        ),
    )


def update_distance(
    flight_number,
    distance,
):
    """
    Update the distance of a flight.

    Parameters
    ----------
    flight_number : str
        Flight number to update.

    distance : float
        New flight distance.

    Returns
    -------
    int
        Number of affected rows.
    """

    if not flight_number:
        raise ValueError("Flight number is required.")

    return execute_query(
        UPDATE_DISTANCE,
        (
            distance,
            str(flight_number).strip(),
        ),
    )


# ==========================================================
# SAVE / UPDATE RUNWAY PERFORMANCE
# ==========================================================


def save_runway_performance(
    flight_number,
    airport_code,
    runway_id,
    required_takeoff_distance,
    required_landing_distance,
    takeoff_margin,
    landing_margin,
    takeoff_status,
    landing_status,
    temperature,
    aircraft_weight=None,
    reference_weight=None,
    connection=None,
):
    """
    Insert or update runway performance for one flight.

    Version 5 stores runway performance in the dedicated
    ``flight_runway_performance`` table rather than in
    ``flights``.

    Returns
    -------
    int
        Number of affected rows.
    """

    if not flight_number:
        raise ValueError("Flight number is required.")

    if not airport_code:
        raise ValueError("Airport code is required.")

    if not runway_id:
        raise ValueError("Runway ID is required.")

    parameters = (
        str(flight_number).strip(),
        str(airport_code).strip().upper(),
        str(runway_id).strip().upper(),
        str(airport_code).strip().upper(),
        required_takeoff_distance,
        required_landing_distance,
        takeoff_margin,
        landing_margin,
        takeoff_status,
        landing_status,
        temperature,
        aircraft_weight,
        reference_weight,
    )

    if connection is not None:
        cursor = connection.cursor()
        cursor.execute(UPSERT_RUNWAY_PERFORMANCE, parameters)
        return cursor.rowcount

    return execute_query(
        UPSERT_RUNWAY_PERFORMANCE,
        parameters,
    )
