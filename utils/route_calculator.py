"""
AeroFlight Suite
Route Calculation Utilities

Provides geographic calculations used by the
flight route and distance services.
"""

from math import atan2
from math import cos
from math import radians
from math import sin
from math import sqrt

from config.config import EARTH_RADIUS_KM
from utils.validation import (
    validate_latitude,
    validate_longitude,
)


def calculate_distance(
    lat1,
    lon1,
    lat2,
    lon2,
):
    """
    Calculate the great-circle distance between
    two geographic coordinates using the Haversine formula.

    Parameters
    ----------
    lat1 : float
        Latitude of the departure airport in degrees.

    lon1 : float
        Longitude of the departure airport in degrees.

    lat2 : float
        Latitude of the arrival airport in degrees.

    lon2 : float
        Longitude of the arrival airport in degrees.

    Returns
    -------
    float
        Distance between the two points in kilometers,
        rounded according to DECIMAL_PRECISION.

    Raises
    ------
    ValueError
        If any coordinate is outside its valid geographic range.
    """

    lat1 = validate_latitude(
        lat1,
    )

    lon1 = validate_longitude(
        lon1,
    )

    lat2 = validate_latitude(
        lat2,
    )

    lon2 = validate_longitude(
        lon2,
    )

    latitude_1 = radians(lat1)
    longitude_1 = radians(lon1)

    latitude_2 = radians(lat2)
    longitude_2 = radians(lon2)

    delta_latitude = latitude_2 - latitude_1
    delta_longitude = longitude_2 - longitude_1

    haversine_value = (
        sin(delta_latitude / 2) ** 2
        + cos(latitude_1) * cos(latitude_2) * sin(delta_longitude / 2) ** 2
    )

    # Protect against extremely small floating-point
    # errors that could make the value slightly exceed 1.
    haversine_value = min(
        1.0,
        max(
            0.0,
            haversine_value,
        ),
    )

    central_angle = 2 * atan2(
        sqrt(haversine_value),
        sqrt(1 - haversine_value),
    )

    distance = EARTH_RADIUS_KM * central_angle

    return round(
        distance,
        2,
    )
