from config.config import LINE_XLARGE
from utils.display import (
    print_title,
    display_flights_table,
)
from database.database_manager import get_all_flights


def show_history():
    flights = get_all_flights()

    print_title("FLIGHT HISTORY", LINE_XLARGE)

    if not flights:
        print("No flights found.")
        print("=" * LINE_XLARGE)
        return

    display_flights_table(flights)

    print("=" * LINE_XLARGE)
