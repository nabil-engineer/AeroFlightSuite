def calculate_flight_time(distance, speed):
    """
    Calculate the flight duration in hours.

    Args:
        distance (float): Flight distance in kilometers.
        speed (float): Aircraft speed in km/h.

    Returns:
        float: Flight duration in hours.
    """
    return distance / speed


def calculate_fuel_needed(distance, fuel_consumption):
    """
    Calculate the total fuel required for the flight.

    Args:
        distance (float): Flight distance in kilometers.
        fuel_consumption (float): Fuel consumption in liters per kilometer.

    Returns:
        float: Total fuel required in liters.
    """
    return distance * fuel_consumption


def calculate_fuel_cost(fuel_needed, fuel_price):
    """
    Calculate the total fuel cost.

    Args:
        fuel_needed (float): Total fuel required.
        fuel_price (float): Fuel price per liter.

    Returns:
        float: Total fuel cost.
    """
    return fuel_needed * fuel_price

