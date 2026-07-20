from config.config import LINE_LARGE
from utils.display import (
    print_title,
    display_flights_table,
)
from database.database_manager import (
    search_flights,
    advanced_search,
    filter_flights,
    sort_flights,
    backup_database,
)


def show_results(title, flights):
    print_title(title, LINE_LARGE)
    display_flights_table(flights)


def show_menu(title, options):
    print_title(title, LINE_LARGE)

    for key, value in options.items():
        print(f"{key}. {value}")


def search_flight():

    keyword = input("\nSearch (Flight, Pilot, Aircraft, Route, Status): ").strip()

    if not keyword:
        print("\nSearch cannot be empty.")
        return

    show_results(
        "SEARCH RESULTS",
        search_flights(keyword),
    )


def advanced_flight_search():

    filters = {
        "flight_number": input("Flight Number: ").strip(),
        "pilot": input("Pilot Name: ").strip(),
        "aircraft": input("Aircraft: ").strip(),
        "departure": input("Departure City: ").strip(),
        "arrival": input("Arrival City: ").strip(),
        "status": input("Status: ").strip(),
    }

    show_results(
        "ADVANCED SEARCH",
        advanced_search(**filters),
    )


def filter_menu():

    options = {
        "1": "Status",
        "2": "Distance",
        "3": "Back",
    }

    show_menu("FLIGHT FILTER", options)

    choice = input("\nChoose option: ")

    if choice == "1":

        flights = filter_flights(
            "status",
            input("Status: ").strip(),
        )

    elif choice == "2":

        try:
            distance = float(input("Minimum Distance: "))

        except ValueError:
            print("Invalid number.")
            return

        flights = filter_flights(
            "distance",
            distance,
        )

    elif choice == "3":
        return

    else:
        print("Invalid choice.")
        return

    show_results(
        "FILTER RESULTS",
        flights,
    )


def sort_menu():

    options = {
        "1": ("Date", "date"),
        "2": ("Distance", "distance"),
        "3": ("Fuel Cost", "cost"),
        "4": ("Pilot", "pilot"),
        "5": ("Back", None),
    }

    while True:

        show_menu(
            "SORT FLIGHTS",
            {key: value[0] for key, value in options.items()},
        )

        choice = input("\nChoose option: ")

        if choice == "5":
            return

        if choice not in options:
            print("Invalid choice.")
            continue

        show_results(
            "SORT RESULTS",
            sort_flights(options[choice][1]),
        )


def backup_menu():

    print_title(
        "DATABASE BACKUP",
        LINE_LARGE,
    )

    backup_database()
