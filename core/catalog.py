from data.aircraft_data import aircrafts
from data.airport_data import airports
from config.config import LINE_MEDIUM, LINE_XLARGE

from utils.display import (
    print_title,
    display_aircraft_table,
    display_airport_table,
)


def search_dictionary(data, keyword, fields):
    keyword = keyword.strip().lower()

    return {
        key: item
        for key, item in data.items()
        if any(keyword in str(item[field]).lower() for field in fields)
    }


def show_aircraft_database():

    print_title("AIRCRAFT DATABASE", LINE_MEDIUM)

    display_aircraft_table(aircrafts)



def search_aircraft():

    keyword = input("\nSearch (Manufacturer or Model): ").strip()

    print_title("SEARCH RESULTS", LINE_MEDIUM)

    results = search_dictionary(
        aircrafts,
        keyword,
        ["manufacturer", "model"],
    )

    if results:
        display_aircraft_table(results)
    else:
        print("\nNo aircraft found.")

    print("=" * LINE_MEDIUM)


def show_airport_database():

    print_title("AIRPORT DATABASE", LINE_XLARGE)

    display_airport_table(airports)


def search_airport():

    keyword = input("\nSearch (Code, Airport, City or Country): ").strip()

    print_title("SEARCH RESULTS", LINE_MEDIUM)

    results = search_dictionary(
        airports,
        keyword,
        [
            "name",
            "city",
            "country",
        ],
    )

    if results:
        display_airport_table(results)
    else:
        print("\nNo airport found.")

    print("=" * LINE_MEDIUM)
