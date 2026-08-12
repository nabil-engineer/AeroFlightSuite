from data.aircraft_data import aircrafts
from data.airport_data import airports

from utils.validation import get_input

from utils.display import (
    print_title,
    display_aircraft_table,
    display_airport_table,
)

from config.config import (
    LINE_MEDIUM,
    LINE_XLARGE,
    TITLE_AIRCRAFT_DATABASE,
    TITLE_AIRPORT_DATABASE,
    TITLE_SEARCH_RESULTS,
    MSG_SEARCH_EMPTY,
    MSG_NO_AIRCRAFT_FOUND,
    MSG_NO_AIRPORT_FOUND,
)

def search_dictionary(
    data,
    keyword,
    fields,
    search_key=False,
):
    """
    Generic search engine for dictionary datasets.
    """

    keyword = keyword.strip().casefold()

    if not keyword:
        return {}

    results = {}

    for key, item in data.items():

        if search_key and keyword in str(key).casefold():
            results[key] = item
            continue

        for field in fields:
            value = str(item.get(field, "")).casefold()

            if keyword in value:
                results[key] = item
                break

    return results


def show_aircraft_database():
    """
    Display aircraft database.
    """
    print_title(
        TITLE_AIRCRAFT_DATABASE,
        LINE_MEDIUM,
    )
    display_aircraft_table(aircrafts)


def search_aircraft():
    """
    Search aircraft by manufacturer or model.
    """

    keyword = get_input("\nSearch (Manufacturer or Model): ").strip()

    if not keyword:
        print(f"\n{MSG_SEARCH_EMPTY}")
        return

    print_title(
        TITLE_SEARCH_RESULTS,
        LINE_MEDIUM,
    )

    results = search_dictionary(
        aircrafts,
        keyword,
        [
            "manufacturer",
            "model",
        ],
    )

    if results:
        display_aircraft_table(results)
    else:
        print(f"\n{MSG_NO_AIRCRAFT_FOUND}")

    print("=" * LINE_MEDIUM)


def show_airport_database():
    """
    Display airport database.
    """

    print_title(
        TITLE_AIRPORT_DATABASE,
        LINE_XLARGE,
    )

    display_airport_table(airports)


def search_airport():
    """
    Search airport by code, airport name,
    city or country.
    """

    keyword = get_input("\nSearch (Code, Airport, City or Country): ").strip()

    if not keyword:
        print(f"\n{MSG_SEARCH_EMPTY}")
        return

    print_title(
        TITLE_SEARCH_RESULTS,
        LINE_MEDIUM,
    )

    results = search_dictionary(
        airports,
        keyword,
        [
            "name",
            "city",
            "country",
        ],
        search_key=True,
    )

    if results:
        display_airport_table(results)
    else:
        print(f"\n{MSG_NO_AIRPORT_FOUND}")

    print("=" * LINE_MEDIUM)
