from config.config import (
    LINE_SMALL,
    LINE_MEDIUM,
    LINE_LARGE,
    LINE_XLARGE,
)


def print_title(title, width=LINE_SMALL):
    print("\n" + "=" * width)
    print(f"{title:^{width}}")
    print("=" * width)


def print_separator(width=LINE_SMALL):
    print("-" * width)


def print_table_header(headers, widths):
    """
    Print a formatted table header.
    """
    print()
    print("".join(f"{header:<{width}}" for header, width in zip(headers, widths)))


def pause():
    input("\nPress Enter to continue...")


def display_flights_table(flights):
    if not flights:
        print("\nNo flights found.")
        return

    print_separator(LINE_LARGE)

    print_table_header(
        ["Flight", "Date", "Pilot", "Aircraft", "Route", "Status"],
        [12, 14, 15, 25, 30, 12],
    )

    print_separator(LINE_LARGE)

    for flight in flights:
        aircraft = f"{flight['manufacturer']} {flight['model']}"
        route = f"{flight['departure_city']} -> {flight['arrival_city']}"

        print(
            f"{flight['flight_number']:<12}"
            f"{flight['flight_date']:<14}"
            f"{flight['pilot']:<15}"
            f"{aircraft:<25}"
            f"{route:<30}"
            f"{flight['status']:<12}"
        )

    print_separator(LINE_LARGE)


def display_aircraft_table(aircrafts):

    print_table_header(
        ["No", "Manufacturer", "Model", "Speed", "Fuel(L/km)"],
        [5, 20, 25, 15, 15],
    )

    print("-" * 80)

    for number, aircraft in aircrafts.items():

        print(
            f"{number:<5}"
            f"{aircraft['manufacturer']:<20}"
            f"{aircraft['model']:<25}"
            f"{aircraft['speed']:<15}"
            f"{aircraft['fuel_consumption']:<15}"
        )


def display_airport_table(airports):
    
    print_table_header(
        ["Code", "Airport", "City", "Country"],
        [8, 40, 20, 20],
    )
    print("-" * 95)

    for code, airport in airports.items():

        print(
            f"{code:<8}"
            f"{airport['name']:<40}"
            f"{airport['city']:<20}"
            f"{airport['country']:<20}"
        )
