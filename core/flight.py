from config.config import LINE_SMALL
from utils.display import print_title
from data.aircraft_data import aircrafts
from data.airport_data import airports
from database.database_manager import flight_exists
from managers.file_manager import save_flight
from services.flight_service import create_flight
from utils.route_calculator import calculate_distance
from utils.validation import (
    get_aircraft_choice,
    get_airport_code,
    get_arrival_airport,
    get_flight_date,
    get_pilot_name,
    get_positive_number,
    validate_flight_number,
)

def select_aircraft():
    """
    Return the selected aircraft.
    """
    return aircrafts[get_aircraft_choice(aircrafts)]


def new_flight():
    print("\nStarting a new flight...\n")

    aircraft = select_aircraft()

    display_aircraft_information(
        aircraft["manufacturer"],
        aircraft["model"],
        aircraft["speed"],
        aircraft["fuel_consumption"],
    )

    flight = build_flight(aircraft)

    print_report(flight)

    save_report(flight)


def build_flight(aircraft):
    flight_number, flight_date = get_flight_details()

    (
        pilot,
        departure_code,
        departure_city,
        arrival_code,
        arrival_city,
        distance,
        fuel_price,
    ) = get_flight_information()

    return create_flight(
        flight_number,
        flight_date,
        pilot,
        aircraft,
        departure_code,
        departure_city,
        arrival_code,
        arrival_city,
        distance,
        fuel_price,
    )


def display_aircraft_information(manufacturer, model, speed, fuel_consumption):
    print_title("AIRCRAFT SELECTED", LINE_SMALL)
    print(f"Manufacturer : {manufacturer}")
    print(f"Model        : {model}")
    print(f"Speed        : {speed} km/h")
    print(f"Fuel Rate    : {fuel_consumption} L/km")


def get_flight_details():

    print("\nFlight Information")
    print("------------------------")

    while True:

        flight_number = input("Flight Number: ").strip().upper()

        if not validate_flight_number(flight_number):
            print("Invalid flight number format (example: AT123).")
            continue

        if flight_exists(flight_number):
            print("Flight number already exists.")
            continue

        break

    flight_date = get_flight_date()

    return flight_number, flight_date


def get_flight_information():

    pilot = get_pilot_name("\nPilot Name: ")

    print("\nAvailable Airports\n")

    for code, airport in airports.items():
        print(f"{code} - {airport['city']}")

    departure_code = get_airport_code(airports, "\nDeparture Airport: ")

    arrival_code = get_arrival_airport(
        airports,
        departure_code,
    )

    departure_city = airports[departure_code]["city"]

    arrival_city = airports[arrival_code]["city"]

    distance = calculate_distance(
        airports[departure_code]["latitude"],
        airports[departure_code]["longitude"],
        airports[arrival_code]["latitude"],
        airports[arrival_code]["longitude"],
    )

    print(f"\nCalculated Distance : {distance:.2f} km")

    fuel_price = get_positive_number("Fuel Price (€): ")

    return (
        pilot,
        departure_code,
        departure_city,
        arrival_code,
        arrival_city,
        distance,
        fuel_price,
    )  


def print_report(flight):

    print_title("FLIGHT REPORT", LINE_SMALL)

    print(f"Flight Number  : {flight.flight_number}")
    print(f"Flight Date    : {flight.flight_date}")
    print(f"Pilot          : {flight.pilot}")
    print(f"Aircraft       : {flight.aircraft_name()}")
    print(f"Route          : {flight.route()}")
    print(f"Status         : {flight.status}")

    print("-" * LINE_SMALL)

    print(f"Distance       : {flight.distance} km")
    print(f"Speed          : {flight.speed} km/h")
    print(f"Flight Time    : {flight.flight_time:.2f} hours")

    print("-" * LINE_SMALL)

    print(f"Fuel Needed    : {flight.fuel_needed:.2f} L")
    print(f"Fuel Price     : {flight.fuel_price:.2f} €/L")
    print(f"Fuel Cost      : {flight.fuel_cost:.2f} €")

    print("=" * LINE_SMALL)


def save_report(flight):
    try:
        save_flight(flight)
        print("\nFlight saved successfully.")
    except ValueError as error:
        print(f"\nError: {error}")
