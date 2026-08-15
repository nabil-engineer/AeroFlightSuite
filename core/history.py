"""
AeroFlight Suite
Flight History

Core workflow responsible for displaying
the complete flight history.

Database access is handled through the
flight repository layer.
"""

from config.config import (
    LINE_XLARGE,
    TITLE_FLIGHT_HISTORY,
    MSG_NO_FLIGHTS_FOUND,
)

from utils.display import (
    print_title,
    display_flights_table,
)

from managers.flight_manager import (
    get_all_flights,
)

def show_history():
    """
    Display the complete flight history.

    Flight data is retrieved through the repository
    layer instead of accessing the database layer
    directly.

    Returns
    -------
    None
    """

    flights = get_all_flights()

    print_title(
        TITLE_FLIGHT_HISTORY,
        LINE_XLARGE,
    )

    if not flights:
        print(MSG_NO_FLIGHTS_FOUND)
        print("=" * LINE_XLARGE)
        return

    display_flights_table(
        flights,
    )

    print("=" * LINE_XLARGE)
