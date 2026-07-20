import re
from datetime import datetime

from config.config import (
    DATE_FORMAT,
    FLIGHT_NUMBER_PATTERN,
)

# ==========================================================
# VALIDATION FUNCTIONS
# ==========================================================


def validate_flight_number(flight_number):
    return re.match(FLIGHT_NUMBER_PATTERN, flight_number) is not None


# ==========================================================
# INPUT FUNCTIONS
# ==========================================================


def get_flight_date():
    while True:
        date = input("Flight Date (YYYY-MM-DD): ").strip()

        try:
            datetime.strptime(date, DATE_FORMAT)
            return date
        except ValueError:
            print("Invalid date format.")


def get_positive_number(message):
    while True:

        try:
            value = float(input(message))

            if value > 0:
                return value

            print("Value must be greater than zero.")

        except ValueError:
            print("Invalid number.")


def get_pilot_name(message):
    while True:

        name = input(message).strip()

        if name:
            return name.title()

        print("Pilot name cannot be empty.")


def get_aircraft_choice(aircrafts):

    while True:

        for number, aircraft in aircrafts.items():

            print(f"{number}. " f"{aircraft['manufacturer']} " f"{aircraft['model']}")

        try:

            choice = int(input("\nChoose Aircraft: "))

            if choice in aircrafts:
                return choice

        except ValueError:
            pass

        print("Invalid aircraft selection.")


def get_airport_code(airports, message):

    while True:

        code = input(message).strip().upper()

        if code in airports:
            return code

        print("Airport code not found.")


def get_arrival_airport(airports, departure_code):

    while True:

        arrival = get_airport_code(
            airports,
            "Arrival Airport: ",
        )

        if arrival != departure_code:
            return arrival

        print("Departure and arrival airports cannot be the same.")
