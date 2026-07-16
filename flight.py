from calculator import (
    calculate_flight_time,
    calculate_fuel_needed,
    calculate_fuel_cost
)

from validation import (
    get_pilot_name,
    get_positive_number,
    get_aircraft_choice,
    get_airport_code,
)

from aircraft_data import aircrafts
from airport_data import airports
from route_calculator import calculate_distance
from file_manager import save_flight
from flight_model import Flight
from config import LINE_SMALL

def display_aircrafts():

    print("Available Aircraft:\n")

    for number, aircraft in aircrafts.items():
        print(f"{number}. {aircraft['manufacturer']} {aircraft['model']}")

def select_aircraft():

    choice = get_aircraft_choice(aircrafts)

    return aircrafts[choice]

def new_flight():

    print("\nStarting a new flight...\n")

    display_aircrafts()

    selected_aircraft = select_aircraft()

    (
    manufacturer,
    model,
    speed,
    fuel_consumption
    ) = get_aircraft_information(selected_aircraft)

    display_aircraft_information(
        manufacturer,
        model,
        speed,
        fuel_consumption,
    )

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
    flight_time, fuel_needed, fuel_cost = calculate_flight(
        distance,
        speed,
        fuel_consumption,
        fuel_price,
    )

    status = "Scheduled"
    flight = Flight(
        flight_number,
        flight_date,
        pilot,
        manufacturer,
        model,
        departure_code,
        departure_city,
        arrival_code,
        arrival_city,
        distance,
        speed,
        fuel_price,
        flight_time,
        fuel_needed,
        fuel_cost,
        status,
    )
    print_report(flight)

    save_report(flight)


def get_aircraft_information(selected_aircraft):

    manufacturer = selected_aircraft["manufacturer"]
    model = selected_aircraft["model"]
    speed = selected_aircraft["speed"]
    fuel_consumption = selected_aircraft["fuel_consumption"]

    return manufacturer, model, speed, fuel_consumption  


def display_aircraft_information(manufacturer, model, speed, fuel_consumption):
    print("\nAircraft Selected")
    print("------------------------")
    print(f"Manufacturer : {manufacturer}")
    print(f"Model        : {model}")
    print(f"Speed        : {speed} km/h")
    print(f"Fuel Rate    : {fuel_consumption} L/km")


def get_flight_details():
    print("\nFlight Information")
    print("------------------------")

    flight_number = input("Flight Number: ").strip()
    while not flight_number:
        print("Flight number cannot be empty.")
        flight_number = input("Flight Number: ").strip()

    flight_date = input("Flight Date (YYYY-MM-DD): ").strip()
    while not flight_date:
        print("Flight date cannot be empty.")
        flight_date = input("Flight Date (YYYY-MM-DD): ").strip()

    return flight_number, flight_date


def get_flight_information():

    pilot = get_pilot_name("\nPilot Name: ")

    print("\nAvailable Airports\n")

    for code, airport in airports.items():
        print(f"{code} - {airport['city']}")

    departure_code = get_airport_code(airports, "\nDeparture Airport: ")

    arrival_code = get_airport_code(airports, "Arrival Airport: ")

    departure_city = airports[departure_code]["city"]

    arrival_city = airports[arrival_code]["city"]

    departure_airport = airports[departure_code]

    arrival_airport = airports[arrival_code]

    distance = calculate_distance(
       departure_airport["latitude"],
       departure_airport["longitude"],
       arrival_airport["latitude"],
       arrival_airport["longitude"]
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


def calculate_flight(distance, speed, fuel_consumption, fuel_price):

    flight_time = calculate_flight_time(distance, speed)

    fuel_needed = calculate_fuel_needed(distance, fuel_consumption)

    fuel_cost = calculate_fuel_cost(fuel_needed, fuel_price)

    return flight_time, fuel_needed, fuel_cost   


def print_report(flight):

    print("\n" + "=" * LINE_SMALL)
    print(f"{'FLIGHT REPORT':^{LINE_SMALL}}")
    print("=" * LINE_SMALL)
    print(f"{'FLIGHT REPORT':^{LINE_SMALL}}")
    print("=" * LINE_SMALL)
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

    save_flight(
        flight.flight_number,
        flight.flight_date,
        flight.pilot,
        flight.manufacturer,
        flight.model,
        flight.departure_city,
        flight.arrival_city,
        flight.distance,
        flight.flight_time,
        flight.fuel_needed,
        flight.fuel_cost,
        flight.status,
    )

    print("\nFlight saved successfully.")
