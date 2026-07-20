from config.config import LINE_SMALL
from utils.display import print_title
from database.database_manager import get_statistics


def show_statistics():
    statistics = get_statistics()

    total_flights = statistics[0] or 0
    total_distance = statistics[1] or 0
    total_flight_time = statistics[2] or 0
    total_fuel_needed = statistics[3] or 0
    total_fuel_cost = statistics[4] or 0

    average_flight_time = total_flight_time / total_flights if total_flights else 0

    print_title("FLIGHT STATISTICS", LINE_SMALL)

    print(f"Total Flights       : {total_flights}")
    print(f"Total Distance      : {total_distance:.2f} km")
    print(f"Total Flight Time   : {total_flight_time:.2f} hours")
    print(f"Average Flight Time : {average_flight_time:.2f} hours")
    print(f"Total Fuel Needed   : {total_fuel_needed:.2f} L")
    print(f"Total Fuel Cost     : {total_fuel_cost:.2f} €")

    print("=" * LINE_SMALL)
