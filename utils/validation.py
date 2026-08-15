"""
AeroFlight Suite
Validation Utilities

Version 5.0

Centralized validation and user-input helpers.

Responsibilities
----------------
1. Domain validation
2. Interactive console input
3. Aircraft / airport validation
4. Weather validation
5. Runway validation
6. Runway performance input validation

Design rule
-----------
Business calculations do not belong here.

This module validates, normalizes, and collects
user input only.
"""

import re
from datetime import datetime

from config.config import (
    DATE_FORMAT,
    FLIGHT_NUMBER_PATTERN,
    WIND_DIRECTIONS,
    MIN_TEMPERATURE,
    MAX_TEMPERATURE,
    MAX_WIND_SPEED,
    MIN_PRESSURE,
    MAX_PRESSURE,
    MAX_VISIBILITY,
    MIN_WEATHER_FACTOR,
)

# ==========================================================
# GENERIC VALIDATION
# ==========================================================


def validate_numeric_range(
    value,
    minimum,
    maximum,
    field_name,
):
    """
    Validate a numeric value inside an inclusive range.

    Returns
    -------
    float
        Normalized numeric value.

    Raises
    ------
    ValueError
        If the value is not numeric or outside the range.
    """

    try:
        normalized_value = float(value)

    except (TypeError, ValueError) as error:
        raise ValueError(f"{field_name} must be a number.") from error

    if not (minimum <= normalized_value <= maximum):
        raise ValueError(f"{field_name} must be between " f"{minimum} and {maximum}.")

    return normalized_value


def validate_positive_value(
    value,
    field_name,
):
    """
    Validate that a numeric value is greater than zero.

    Returns
    -------
    float
        Normalized positive value.
    """

    try:
        normalized_value = float(value)

    except (TypeError, ValueError) as error:
        raise ValueError(f"{field_name} must be a number.") from error

    if normalized_value <= 0:
        raise ValueError(f"{field_name} must be greater than zero.")

    return normalized_value


def validate_non_negative_value(
    value,
    field_name,
):
    """
    Validate that a numeric value is zero or greater.

    Returns
    -------
    float
        Normalized numeric value.
    """

    try:
        normalized_value = float(value)

    except (TypeError, ValueError) as error:
        raise ValueError(f"{field_name} must be a number.") from error

    if normalized_value < 0:
        raise ValueError(f"{field_name} cannot be negative.")

    return normalized_value


# ==========================================================
# GEOGRAPHIC VALIDATION
# ==========================================================


def validate_latitude(value):
    """
    Validate latitude.

    Latitude range:
        -90 to 90 degrees.
    """

    return validate_numeric_range(
        value,
        -90,
        90,
        "Latitude",
    )


def validate_longitude(value):
    """
    Validate longitude.

    Longitude range:
        -180 to 180 degrees.
    """

    return validate_numeric_range(
        value,
        -180,
        180,
        "Longitude",
    )


# ==========================================================
# FLIGHT NUMBER
# ==========================================================


def validate_flight_number(flight_number):
    """
    Validate a flight number.

    Returns
    -------
    bool
        True when valid, otherwise False.
    """

    if not isinstance(
        flight_number,
        str,
    ):
        return False

    normalized_flight_number = flight_number.strip().upper()

    if not normalized_flight_number:
        return False

    return (
        re.fullmatch(
            FLIGHT_NUMBER_PATTERN,
            normalized_flight_number,
        )
        is not None
    )


# ==========================================================
# DATE
# ==========================================================


def validate_flight_date(flight_date):
    """
    Validate and normalize a flight date.

    Returns
    -------
    str
        Validated date string.

    Raises
    ------
    ValueError
        If the date is invalid.
    """

    if not isinstance(
        flight_date,
        str,
    ):
        raise ValueError("Flight date must be a string.")

    normalized_date = flight_date.strip()

    if not normalized_date:
        raise ValueError("Flight date cannot be empty.")

    try:
        datetime.strptime(
            normalized_date,
            DATE_FORMAT,
        )

    except ValueError as error:
        raise ValueError("Invalid flight date.") from error

    return normalized_date


# ==========================================================
# INTERACTIVE FLIGHT INPUTS
# ==========================================================


def get_flight_date():
    """
    Ask the user for a valid flight date.
    """

    while True:
        value = input("Flight Date (YYYY-MM-DD): ").strip()

        try:
            return validate_flight_date(
                value,
            )

        except ValueError:
            print("Invalid date format.")


def get_positive_number(
    message,
    minimum=0.0,
):
    """
    Ask the user for a numeric value
    greater than the supplied minimum.
    """

    while True:
        try:
            value = float(input(message).strip())

        except ValueError:
            print("Please enter a valid numeric value.")
            continue

        if value > minimum:
            return value

        print(f"Value must be greater than " f"{minimum}.")


# ==========================================================
# AIRCRAFT / AIRPORT SELECTION
# ==========================================================


def get_aircraft_choice(aircrafts):
    """
    Ask the user to select an aircraft.
    """

    while True:

        for number, aircraft in aircrafts.items():
            print(f"{number}. " f"{aircraft['manufacturer']} " f"{aircraft['model']}")

        try:
            choice = int(input("\nChoose Aircraft: ").strip())

        except ValueError:
            choice = None

        if choice in aircrafts:
            return choice

        print("Invalid aircraft selection.")


def get_airport_code(
    airports,
    message,
):
    """
    Ask for a valid airport code.

    The returned code is always uppercase.
    """

    while True:

        code = input(message).strip().upper()

        if code in airports:
            return code

        print("Airport code not found.")


def get_arrival_airport(
    airports,
    departure_code,
):
    """
    Ask for an arrival airport that differs
    from the departure airport.
    """

    normalized_departure = (
        departure_code.strip().upper()
        if isinstance(
            departure_code,
            str,
        )
        else departure_code
    )

    while True:

        arrival = get_airport_code(
            airports,
            "Arrival Airport: ",
        )

        if arrival != normalized_departure:
            return arrival

        print("Departure and arrival airports " "cannot be the same.")


# ==========================================================
# WEATHER VALIDATION
# ==========================================================


def validate_temperature(value):
    """
    Validate temperature in Celsius.
    """

    return validate_numeric_range(
        value,
        MIN_TEMPERATURE,
        MAX_TEMPERATURE,
        "Temperature",
    )


def validate_wind_speed(value):
    """
    Validate wind speed.

    Zero wind speed is allowed.
    """

    return validate_numeric_range(
        value,
        0,
        MAX_WIND_SPEED,
        "Wind speed",
    )


def validate_pressure(value):
    """
    Validate atmospheric pressure.
    """

    return validate_numeric_range(
        value,
        MIN_PRESSURE,
        MAX_PRESSURE,
        "Pressure",
    )


def validate_humidity(value):
    """
    Validate humidity percentage.
    """

    return validate_numeric_range(
        value,
        0,
        100,
        "Humidity",
    )


def validate_visibility(value):
    """
    Validate visibility.

    Visibility must be greater than zero
    and cannot exceed MAX_VISIBILITY.
    """

    try:
        normalized_value = float(value)

    except (TypeError, ValueError) as error:
        raise ValueError("Visibility must be a number.") from error

    if normalized_value <= 0:
        raise ValueError("Visibility must be greater than 0.")

    if normalized_value > MAX_VISIBILITY:
        raise ValueError(f"Visibility must be between " f"0 and {MAX_VISIBILITY}.")

    return normalized_value


def validate_weather_factor(value):
    """
    Validate weather factor.
    """

    try:
        normalized_value = float(value)

    except (TypeError, ValueError) as error:
        raise ValueError("Weather factor must be a number.") from error

    if normalized_value < MIN_WEATHER_FACTOR:
        raise ValueError("Weather factor cannot be below " f"{MIN_WEATHER_FACTOR}.")

    return normalized_value


def validate_wind_direction(value):
    """
    Validate a wind-direction value.

    Accepts:
    - configured numeric key
    - configured textual value
    """

    if value in WIND_DIRECTIONS:
        return WIND_DIRECTIONS[value]

    if value in WIND_DIRECTIONS.values():
        return value

    raise ValueError("Invalid wind direction.")


# ==========================================================
# INTERACTIVE WEATHER INPUTS
# ==========================================================


def get_wind_direction():
    """
    Ask the user to select wind direction.
    """

    while True:

        print("\nWind Direction")

        for key, value in WIND_DIRECTIONS.items():
            print(f"{key}. {value}")

        choice = input("\nChoose Direction: ").strip()

        try:
            return validate_wind_direction(
                choice,
            )

        except ValueError:
            print("Invalid choice.")


def get_temperature():
    """
    Ask for a valid temperature.
    """

    while True:

        try:
            value = float(input("Temperature (°C): ").strip())

            return validate_temperature(
                value,
            )

        except ValueError as error:
            print(error)


def get_wind_speed():
    """
    Ask for a valid wind speed.
    """

    while True:

        try:
            value = float(input("Wind Speed (km/h): ").strip())

            return validate_wind_speed(
                value,
            )

        except ValueError as error:
            print(error)


def get_pressure():
    """
    Ask for valid atmospheric pressure.
    """

    while True:

        try:
            value = float(input("Pressure (hPa): ").strip())

            return validate_pressure(
                value,
            )

        except ValueError as error:
            print(error)


def get_visibility():
    """
    Ask for valid visibility.
    """

    while True:

        try:
            value = float(input("Visibility (km): ").strip())

            return validate_visibility(
                value,
            )

        except ValueError as error:
            print(error)


def get_humidity():
    """
    Ask for valid humidity.
    """

    while True:

        try:
            value = float(input("Humidity (%): ").strip())

            return validate_humidity(
                value,
            )

        except ValueError as error:
            print(error)


# ==========================================================
# RUNWAY VALIDATION — VERSION 5
# ==========================================================


def validate_airport_elevation(value):
    """
    Validate airport/runway elevation in meters.

    Elevation may be zero for airports at sea level.

    Returns
    -------
    float
        Validated elevation in meters.
    """

    return validate_non_negative_value(
        value,
        "Airport elevation",
    )


def validate_runway_length(value):
    """
    Validate runway length in meters.

    Runway length must be greater than zero.

    Returns
    -------
    float
        Validated runway length in meters.
    """

    return validate_positive_value(
        value,
        "Runway length",
    )


def validate_runway_surface(value):
    """
    Validate and normalize runway surface.

    Supported surfaces correspond to the
    Version 5 performance service.

    Returns
    -------
    str
        Normalized runway surface.
    """

    if not isinstance(
        value,
        str,
    ):
        raise ValueError("Runway surface must be a string.")

    normalized_surface = value.strip().lower()

    allowed_surfaces = {
        "asphalt",
        "concrete",
        "grass",
        "gravel",
        "wet",
    }

    if normalized_surface not in allowed_surfaces:
        raise ValueError(
            "Unsupported runway surface. "
            "Allowed surfaces: "
            "asphalt, concrete, grass, gravel, wet."
        )

    return normalized_surface


def validate_runway_id(value):
    """
    Validate a runway identifier.

    Examples:
        09/27
        18/36
        12L/30R
    """

    if not isinstance(
        value,
        str,
    ):
        raise ValueError("Runway ID must be a string.")

    normalized_value = value.strip().upper()

    if not normalized_value:
        raise ValueError("Runway ID cannot be empty.")

    if len(normalized_value) > 20:
        raise ValueError("Runway ID is too long.")

    return normalized_value


def validate_runway_airport_code(value):
    """
    Validate an airport code associated
    with a runway.

    The V5 runway model uses airport codes
    as the primary airport reference.
    """

    if not isinstance(
        value,
        str,
    ):
        raise ValueError("Airport code must be a string.")

    normalized_code = value.strip().upper()

    if not normalized_code:
        raise ValueError("Airport code cannot be empty.")

    if not re.fullmatch(
        r"[A-Z0-9]{3,4}",
        normalized_code,
    ):
        raise ValueError("Airport code must contain " "3 or 4 letters/numbers.")

    return normalized_code


# ==========================================================
# RUNWAY PERFORMANCE VALIDATION
# ==========================================================


def validate_takeoff_distance(value):
    """
    Validate a base/reference takeoff distance.

    Returns
    -------
    float
        Validated distance in meters.
    """

    return validate_positive_value(
        value,
        "Base takeoff distance",
    )


def validate_landing_distance(value):
    """
    Validate a base/reference landing distance.

    Returns
    -------
    float
        Validated distance in meters.
    """

    return validate_positive_value(
        value,
        "Base landing distance",
    )


def validate_aircraft_weight(value):
    """
    Validate aircraft weight in kilograms.

    Returns
    -------
    float
        Validated aircraft weight.
    """

    return validate_positive_value(
        value,
        "Aircraft weight",
    )


def validate_reference_weight(value):
    """
    Validate reference aircraft weight
    in kilograms.

    Returns
    -------
    float
        Validated reference weight.
    """

    return validate_positive_value(
        value,
        "Reference weight",
    )


def validate_runway_performance_inputs(
    runway_length,
    elevation,
    surface,
):
    """
    Validate the core runway-performance inputs.

    This helper does not perform calculations.

    Returns
    -------
    dict
        Normalized runway performance values.
    """

    return {
        "runway_length": validate_runway_length(
            runway_length,
        ),
        "elevation": validate_airport_elevation(
            elevation,
        ),
        "surface": validate_runway_surface(
            surface,
        ),
    }


# ==========================================================
# GENERIC INPUT
# ==========================================================


def get_input(
    prompt,
    upper=False,
):
    """
    Read and normalize generic user input.

    Parameters
    ----------
    prompt : str
        Input prompt.

    upper : bool
        Convert the result to uppercase.

    Returns
    -------
    str
        Cleaned user input.
    """

    value = input(prompt).strip()

    if upper:
        value = value.upper()

    return value
