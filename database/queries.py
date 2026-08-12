"""
AeroFlight Suite
Central SQL Definitions

All reusable SQL statements used by the
database query modules are defined here.

Architecture
------------
Database query definitions are kept centralized
so read/update/delete modules do not duplicate
SQL statements.

Fuel Contract
-------------
fuel_needed
    Canonical AeroFlight Suite domain field.

fuel_consumption
    Legacy compatibility field retained for
    older databases and historical records.

New application logic must use fuel_needed.
"""

# ==========================================================
# GET ALL FLIGHTS
# ==========================================================

GET_ALL_FLIGHTS = """
SELECT *
FROM flights
ORDER BY id DESC
"""


# ==========================================================
# STATISTICS
# ==========================================================

GET_STATISTICS = """
SELECT

    COUNT(*) AS total_flights,

    COALESCE(
        SUM(distance),
        0
    ) AS total_distance,

    COALESCE(
        SUM(flight_time),
        0
    ) AS total_flight_time,

    COALESCE(
        SUM(
            CASE
                WHEN fuel_needed IS NOT NULL
                    THEN fuel_needed

                WHEN fuel_needed IS NULL
                     AND fuel_consumption IS NOT NULL
                    THEN fuel_consumption

                ELSE 0
            END
        ),
        0
    ) AS total_fuel,

    COALESCE(
        SUM(fuel_cost),
        0
    ) AS total_cost

FROM flights
"""

# ==========================================================
# DELETE FLIGHT
# ==========================================================

DELETE_FLIGHT = """
DELETE FROM flights
WHERE flight_number = ?
"""


# ==========================================================
# UPDATE STATUS
# ==========================================================

UPDATE_STATUS = """
UPDATE flights
SET status = ?
WHERE flight_number = ?
"""


# ==========================================================
# UPDATE DISTANCE
# ==========================================================

UPDATE_DISTANCE = """
UPDATE flights
SET distance = ?
WHERE flight_number = ?
"""


# ==========================================================
# UPDATE FUEL COST
# ==========================================================

UPDATE_FUEL_COST = """
UPDATE flights
SET fuel_cost = ?
WHERE flight_number = ?
"""


# ==========================================================
# UPDATE WEATHER
# ==========================================================

UPDATE_WEATHER = """
UPDATE flights
SET

    weather_factor = ?,

    wind_speed = ?,

    wind_direction = ?,

    temperature = ?,

    pressure = ?,

    humidity = ?,

    visibility = ?,

    weather_condition = ?,

    weather_severity = ?

WHERE flight_number = ?
"""
