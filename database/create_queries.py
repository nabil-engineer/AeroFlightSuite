import sqlite3

from .common import get_connection

def create_database():
    """
    Create the flights table if it does not exist.
    """
    with get_connection() as connection:

        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS flights (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                flight_number TEXT NOT NULL UNIQUE,

                flight_date TEXT NOT NULL,

                pilot TEXT NOT NULL,

                manufacturer TEXT NOT NULL,

                model TEXT NOT NULL,

                departure_code TEXT NOT NULL,

                departure_city TEXT NOT NULL,

                arrival_code TEXT NOT NULL,

                arrival_city TEXT NOT NULL,

                distance REAL NOT NULL,

                speed REAL NOT NULL,

                fuel_price REAL NOT NULL,

                flight_time REAL NOT NULL,

                fuel_needed REAL NOT NULL,

                fuel_cost REAL NOT NULL,

                status TEXT NOT NULL

            )
        """)


def insert_flight(
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
):

    try:

        with get_connection() as connection:

            cursor = connection.cursor()

            cursor.execute(
                """
                INSERT INTO flights(

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
                    status

                )

                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                """,
                (
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
                ),
            )

    except sqlite3.IntegrityError:

        raise ValueError(f"Flight number '{flight_number}' already exists.")
