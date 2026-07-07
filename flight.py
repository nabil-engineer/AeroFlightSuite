from calculator import (
    calculate_flight_time,
    calculate_fuel_needed,
    calculate_fuel_cost
)

from validation import (
    validate_pilot_name,
    validate_positive_number,
    get_positive_number,
    get_city_name,
    get_aircraft_choice
)

from aircraft_data import aircrafts
from file_manager import save_flight
from flight_model import Flight

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
    
    print("\nAircraft Selected")
    print("------------------------")
    print(f"Manufacturer : {manufacturer}")
    print(f"Model        : {model}")
    print(f"Speed        : {speed} km/h")
    print(f"Fuel Rate    : {fuel_consumption} L/km")  

    pilot, departure_city, arrival_city, distance, fuel_price = get_flight_information()
    flight_time, fuel_needed, fuel_cost = calculate_flight(
    distance,
    speed,
    fuel_consumption,
    fuel_price
)
    flight = Flight(
    pilot,
    manufacturer,
    model,
    departure_city,
    arrival_city,
    distance,
    speed,
    fuel_price,
    flight_time,
    fuel_needed,
    fuel_cost
)
    print_report(flight)

    save_report(flight)
    

    


def get_aircraft_information(selected_aircraft):

    manufacturer = selected_aircraft["manufacturer"]
    model = selected_aircraft["model"]
    speed = selected_aircraft["speed"]
    fuel_consumption = selected_aircraft["fuel_consumption"]

    return manufacturer, model, speed, fuel_consumption    

def get_flight_information():

    pilot = input("\nPilot Name: ")

    while not validate_pilot_name(pilot):
        print("Pilot name cannot be empty.")
        pilot = input("Pilot Name: ")

    departure_city = get_city_name("Departure City: ")

    arrival_city = get_city_name("Arrival City: ")

    distance = get_positive_number("Distance (km): ")

    fuel_price = get_positive_number("Fuel Price (€): ")


    return (
        pilot,
        departure_city,
        arrival_city,
        distance,
        fuel_price
    ) 

def calculate_flight(distance, speed, fuel_consumption, fuel_price):

    flight_time = calculate_flight_time(distance, speed)

    fuel_needed = calculate_fuel_needed(distance, fuel_consumption)

    fuel_cost = calculate_fuel_cost(fuel_needed, fuel_price)

    return flight_time, fuel_needed, fuel_cost   

    
def print_report(flight):

    print("\n" + "=" * 60)
    print("                 FLIGHT REPORT")
    print("=" * 60)

    print(f"Pilot          : {flight.pilot}")
    print(f"Aircraft       : {flight.aircraft_name()}")
    print(f"Route          : {flight.route()}")

    print("-" * 60)

    print(f"Distance       : {flight.distance} km")
    print(f"Speed          : {flight.speed} km/h")
    print(f"Flight Time    : {flight.flight_time:.2f} hours")

    print("-" * 60)

    print(f"Fuel Needed    : {flight.fuel_needed:.2f} L")
    print(f"Fuel Price     : {flight.fuel_price:.2f} €/L")
    print(f"Fuel Cost      : {flight.fuel_cost:.2f} €")

    print("=" * 60)

def save_report(flight):

    save_flight(
    flight.pilot,
    flight.manufacturer,
    flight.model,
    flight.departure_city,
    flight.arrival_city,
    flight.distance,
    flight.flight_time,
    flight.fuel_needed,
    flight.fuel_cost
)

    
    print("\nFlight saved successfully.")
    