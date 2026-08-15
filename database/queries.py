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

# ==========================================================
# RUNWAY REFERENCE DATA
# ==========================================================

INSERT_RUNWAY = """
INSERT INTO runways (
    airport_code,
    runway_id,
    length,
    width,
    surface,
    elevation,
    heading
)
VALUES (?, ?, ?, ?, ?, ?, ?)
"""

GET_ALL_RUNWAYS = """
SELECT
    id,
    airport_code,
    runway_id,
    length,
    width,
    surface,
    elevation,
    heading
FROM runways
ORDER BY airport_code, runway_id
"""

GET_RUNWAYS_BY_AIRPORT = """
SELECT
    id,
    airport_code,
    runway_id,
    length,
    width,
    surface,
    elevation,
    heading
FROM runways
WHERE airport_code = ?
ORDER BY runway_id
"""

GET_RUNWAY = """
SELECT
    id,
    airport_code,
    runway_id,
    length,
    width,
    surface,
    elevation,
    heading
FROM runways
WHERE airport_code = ?
  AND runway_id = ?
LIMIT 1
"""

# ==========================================================
# RUNWAY PERFORMANCE
# ==========================================================

UPSERT_RUNWAY_PERFORMANCE = """
INSERT INTO flight_runway_performance (
    flight_id,
    runway_id,
    airport_code,
    required_takeoff_distance,
    required_landing_distance,
    takeoff_margin,
    landing_margin,
    takeoff_status,
    landing_status,
    temperature,
    aircraft_weight,
    reference_weight
)
VALUES (
    (SELECT id FROM flights WHERE flight_number = ?),
    (
        SELECT id
        FROM runways
        WHERE airport_code = ?
          AND runway_id = ?
    ),
    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
)
ON CONFLICT(flight_id) DO UPDATE SET
    runway_id = excluded.runway_id,
    airport_code = excluded.airport_code,
    required_takeoff_distance = excluded.required_takeoff_distance,
    required_landing_distance = excluded.required_landing_distance,
    takeoff_margin = excluded.takeoff_margin,
    landing_margin = excluded.landing_margin,
    takeoff_status = excluded.takeoff_status,
    landing_status = excluded.landing_status,
    temperature = excluded.temperature,
    aircraft_weight = excluded.aircraft_weight,
    reference_weight = excluded.reference_weight
"""

GET_RUNWAY_PERFORMANCE = """
SELECT
    f.flight_number,
    p.id AS performance_id,
    p.flight_id,
    p.airport_code,
    r.id AS runway_db_id,
    r.runway_id,
    r.length AS runway_length,
    r.width AS runway_width,
    r.surface AS runway_surface,
    r.elevation AS runway_elevation,
    r.heading AS runway_heading,
    p.required_takeoff_distance,
    p.required_landing_distance,
    p.takeoff_margin,
    p.landing_margin,
    p.takeoff_status,
    p.landing_status,
    p.temperature,
    p.aircraft_weight,
    p.reference_weight,
    CASE WHEN p.takeoff_margin >= 0 THEN 1 ELSE 0 END
        AS takeoff_sufficient,
    CASE WHEN p.landing_margin >= 0 THEN 1 ELSE 0 END
        AS landing_sufficient
FROM flight_runway_performance AS p
JOIN flights AS f
    ON f.id = p.flight_id
LEFT JOIN runways AS r
    ON r.id = p.runway_id
WHERE f.flight_number = ?
LIMIT 1
"""

DELETE_RUNWAY_PERFORMANCE = """
DELETE FROM flight_runway_performance
WHERE flight_id = (
    SELECT id FROM flights WHERE flight_number = ?
)
"""
