from config.config import DEFAULT_STATUS
from models.flight_model import Flight

from utils.calculator import (
    calculate_flight_time,
    calculate_fuel_needed,
    calculate_fuel_cost,
)


def create_flight(
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
):
    """
    Build and return a Flight object.
    """

    speed = aircraft["speed"]
    fuel_rate = aircraft["fuel_consumption"]

    flight_time = calculate_flight_time(distance, speed)
    fuel_needed = calculate_fuel_needed(distance, fuel_rate)
    fuel_cost = calculate_fuel_cost(fuel_needed, fuel_price)

    return Flight(
        flight_number,
        flight_date,
        pilot,
        aircraft["manufacturer"],
        aircraft["model"],
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
        DEFAULT_STATUS,
    )
