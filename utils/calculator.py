"""
AeroFlight Suite
Calculation Utilities

Centralized calculation functions used by the
application's service and manager layers.
"""

from config.config import DECIMAL_PRECISION
from utils.validation import validate_positive_value


def calculate_flight_time(
    distance,
    speed,
):
    """
    Calculate flight duration in hours.

    Parameters
    ----------
    distance : float
        Flight distance in kilometers.
    speed : float
        Aircraft cruise speed in km/h.

    Returns
    -------
    float
        Flight duration in hours rounded according
        to DECIMAL_PRECISION.

    Raises
    ------
    ValueError
        If distance or speed is invalid.
    """

    distance = validate_positive_value(
        distance,
        "Distance",
    )

    speed = validate_positive_value(
        speed,
        "Speed",
    )

    return round(
        distance / speed,
        DECIMAL_PRECISION,
    )


def calculate_fuel_needed(
    distance,
    fuel_consumption,
    weather_factor=1.0,
):
    """
    Calculate total fuel required.

    Parameters
    ----------
    distance : float
        Flight distance in kilometers.

    fuel_consumption : float
        Fuel consumption in liters per kilometer.

    weather_factor : float, optional
        Weather correction factor.

    Returns
    -------
    float
        Total required fuel rounded according
        to DECIMAL_PRECISION.

    Raises
    ------
    ValueError
        If one of the parameters is invalid.
    """

    distance = validate_positive_value(
        distance,
        "Distance",
    )

    fuel_consumption = validate_positive_value(
        fuel_consumption,
        "Fuel consumption",
    )

    weather_factor = validate_positive_value(
        weather_factor,
        "Weather factor",
    )

    base_fuel = distance * fuel_consumption

    corrected_fuel = base_fuel * weather_factor

    return round(
        corrected_fuel,
        DECIMAL_PRECISION,
    )


def calculate_fuel_cost(
    fuel_needed,
    fuel_price,
):
    """
    Calculate total fuel cost.

    Parameters
    ----------
    fuel_needed : float
        Fuel required in liters.

    fuel_price : float
        Fuel price per liter.

    Returns
    -------
    float
        Total fuel cost rounded according
        to DECIMAL_PRECISION.

    Raises
    ------
    ValueError
        If fuel amount or fuel price is invalid.
    """

    fuel_needed = validate_positive_value(
        fuel_needed,
        "Fuel needed",
    )

    try:
        fuel_price = float(fuel_price)
    except (TypeError, ValueError) as error:
        raise ValueError("Fuel price must be a number.") from error

    if fuel_price < 0:
        raise ValueError("Fuel price cannot be negative.")

    return round(
        fuel_needed * fuel_price,
        DECIMAL_PRECISION,
    )
