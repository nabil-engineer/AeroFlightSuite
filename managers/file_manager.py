from database.database_manager import insert_flight


def save_flight(flight):

    insert_flight(
        flight.flight_number,
        flight.flight_date,
        flight.pilot,
        flight.manufacturer,
        flight.model,
        flight.departure_code,
        flight.departure_city,
        flight.arrival_code,
        flight.arrival_city,
        flight.distance,
        flight.speed,
        flight.fuel_price,
        flight.flight_time,
        flight.fuel_needed,
        flight.fuel_cost,
        flight.status,
    )
