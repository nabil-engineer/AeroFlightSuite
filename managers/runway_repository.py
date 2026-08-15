"""
AeroFlight Suite
Runway Repository

Version 5.0

Repository responsible for retrieving runway domain objects
from the static runway reference data.

Responsibilities
----------------
- Retrieve all runways for an airport
- Retrieve a specific runway
- Check runway availability
- Convert raw runway data into Runway objects

This repository does not perform runway calculations.

Runway calculations belong to services/runway_service.py.
"""

from data.runway_data import runways
from models.runway_model import Runway

# ============================================================
# RUNWAY COLLECTION
# ============================================================


def get_runways(airport_code):
    """
    Return all runways belonging to an airport.

    Parameters
    ----------
    airport_code : str
        ICAO/IATA airport code.

    Returns
    -------
    list[Runway]
        List of runway objects.

    Examples
    --------
    CMN
        -> [Runway(...), Runway(...)]

    RBA
        -> [Runway(...)]
    """

    if airport_code is None:
        return []

    normalized_code = str(airport_code).strip().upper()

    if not normalized_code:
        return []

    airport_runways = runways.get(
        normalized_code,
        [],
    )

    return [
        Runway(
            airport_code=normalized_code,
            runway_id=data.get("runway_id"),
            length=data.get("length"),
            width=data.get("width"),
            surface=data.get("surface"),
            elevation=data.get("elevation"),
            heading=data.get("heading"),
        )
        for data in airport_runways
    ]


# ============================================================
# SINGLE RUNWAY
# ============================================================


def get_runway(
    airport_code,
    runway_id,
):
    """
    Return a specific runway belonging to an airport.

    Parameters
    ----------
    airport_code : str
        Airport code.

    runway_id : str
        Runway identifier.

    Returns
    -------
    Runway or None
        Matching runway if found.
    """

    if airport_code is None or runway_id is None:
        return None

    normalized_code = str(airport_code).strip().upper()

    normalized_runway_id = str(runway_id).strip().upper()

    for runway in get_runways(normalized_code):

        if runway.runway_id == normalized_runway_id:
            return runway

    return None


# ============================================================
# AIRPORT CHECK
# ============================================================


def airport_has_runways(airport_code):
    """
    Check whether an airport has runway data.

    Parameters
    ----------
    airport_code : str
        Airport code.

    Returns
    -------
    bool
        True if at least one runway exists.
    """

    return bool(get_runways(airport_code))


# ============================================================
# RUNWAY COUNT
# ============================================================


def get_runway_count(airport_code):
    """
    Return the number of runways available for an airport.

    Parameters
    ----------
    airport_code : str
        Airport code.

    Returns
    -------
    int
        Number of available runways.
    """

    return len(get_runways(airport_code))


# ============================================================
# ALL RUNWAYS
# ============================================================


def get_all_runways():
    """
    Return all runway objects from the reference dataset.

    Returns
    -------
    list[Runway]
        All available runway objects.
    """

    all_runways = []

    for airport_code in runways:
        all_runways.extend(get_runways(airport_code))

    return all_runways
