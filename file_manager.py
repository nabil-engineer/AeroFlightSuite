import csv
import os

def save_flight(
    pilot,
    manufacturer,
    model,
    departure_city,
    arrival_city,
    distance,
    flight_time,
    fuel_needed,
    fuel_cost
):
    os.makedirs("data", exist_ok=True)
    
    file_exists = os.path.exists("data/flights.csv")

    with open("data/flights.csv", "a", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        if not file_exists:

            writer.writerow([
                "Pilot",
                "Manufacturer",
                "Model",
                "Departure",
                "Arrival",
                "Distance",
                "Flight Time",
                "Fuel Needed",
                "Fuel Cost"
            ])

        writer.writerow([
            pilot,
            manufacturer,
            model,
            departure_city,
            arrival_city,
            distance,
            round(flight_time, 2),
            round(fuel_needed, 2),
            round(fuel_cost, 2)
        ])
        