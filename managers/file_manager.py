import csv
import os

from config.config import CSV_FILE

def save_flight(
    flight_number,
    flight_date,
    pilot,
    manufacturer,
    model,
    departure_city,
    arrival_city,
    distance,
    flight_time,
    fuel_needed,
    fuel_cost,
    status,
):
    os.makedirs("data", exist_ok=True)

    file_exists = os.path.exists(CSV_FILE)

    with open(CSV_FILE, "a", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        if not file_exists:

            writer.writerow(
                [
                    "Flight Number",
                    "Flight Date",
                    "Pilot",
                    "Manufacturer",
                    "Model",
                    "Departure",
                    "Arrival",
                    "Distance",
                    "Flight Time",
                    "Fuel Needed",
                    "Fuel Cost",
                    "Status",
                ]
            )

        writer.writerow(
            [
                flight_number,
                flight_date,
                pilot,
                manufacturer,
                model,
                departure_city,
                arrival_city,
                distance,
                round(flight_time, 2),
                round(fuel_needed, 2),
                round(fuel_cost, 2),
                status,
            ]
        )
