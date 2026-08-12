"""
AeroFlight Suite
Flight Statistics

Application layer responsible for displaying
global flight statistics.

Architecture
------------

Core Statistics
        ↓
Flight Repository
        ↓
Database Manager
        ↓
SQLite

The core layer does not access SQLite directly.

Fuel Contract
-------------
fuel_needed is the canonical flight-level fuel value.

The repository already normalizes legacy
fuel_consumption data into the statistics result.
"""

from config.config import (
    LINE_SMALL,
    TITLE_FLIGHT_STATISTICS,
)

from utils.display import (
    print_title,
)

from managers.flight_repository import (
    get_statistics,
)


def show_statistics():
    """
    Display global flight statistics.

    The repository returns a normalized dictionary.

    Expected structure
    ------------------
    {
        "total_flights": int,
        "total_distance": float,
        "total_flight_time": float,
        "total_fuel": float,
        "total_cost": float,
    }

    Returns
    -------
    None
        Statistics are displayed directly to the user.
    """

    statistics = get_statistics()

    # ======================================================
    # NORMALIZED STATISTICS
    # ======================================================

    total_flights = (
        statistics.get(
            "total_flights",
            0,
        )
        or 0
    )

    total_distance = (
        statistics.get(
            "total_distance",
            0,
        )
        or 0
    )

    total_flight_time = (
        statistics.get(
            "total_flight_time",
            0,
        )
        or 0
    )

    total_fuel = (
        statistics.get(
            "total_fuel",
            0,
        )
        or 0
    )

    total_cost = (
        statistics.get(
            "total_cost",
            0,
        )
        or 0
    )

    # ======================================================
    # NUMERIC NORMALIZATION
    # ======================================================

    try:
        total_flights = int(total_flights)
    except (
        TypeError,
        ValueError,
    ):
        total_flights = 0

    try:
        total_distance = float(total_distance)
    except (
        TypeError,
        ValueError,
    ):
        total_distance = 0.0

    try:
        total_flight_time = float(total_flight_time)
    except (
        TypeError,
        ValueError,
    ):
        total_flight_time = 0.0

    try:
        total_fuel = float(total_fuel)
    except (
        TypeError,
        ValueError,
    ):
        total_fuel = 0.0

    try:
        total_cost = float(total_cost)
    except (
        TypeError,
        ValueError,
    ):
        total_cost = 0.0

    # ======================================================
    # AVERAGE FLIGHT TIME
    # ======================================================

    if total_flights > 0:

        average_flight_time = total_flight_time / total_flights

    else:

        average_flight_time = 0.0

    # ======================================================
    # DISPLAY
    # ======================================================

    print_title(
        TITLE_FLIGHT_STATISTICS,
        LINE_SMALL,
    )

    print(f"Total Flights          : " f"{total_flights}")

    print(f"Total Distance         : " f"{total_distance:.2f} km")

    print(f"Total Flight Time      : " f"{total_flight_time:.2f} hours")

    print(f"Average Flight Time    : " f"{average_flight_time:.2f} hours")

    print(f"Total Fuel Needed      : " f"{total_fuel:.2f}")

    print(f"Total Fuel Cost        : " f"{total_cost:.2f} €")

    print("=" * LINE_SMALL)
