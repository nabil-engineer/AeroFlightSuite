"""
AeroFlight Suite
Aircraft Reference Data

Centralized aircraft reference data used by
flight calculations and Version 5 runway performance.

Architecture
------------
Aircraft Reference Data
        |
        +--> Flight Service
        |
        +--> Runway Performance Service

Data Contract
-------------
Every aircraft record contains the legacy flight
calculation fields:

    manufacturer
    model
    speed
    fuel_consumption

Version 5 additionally requires:

    takeoff_distance
    landing_distance
    reference_weight

The runway performance values are simplified reference
values intended for software simulation and portfolio
purposes. They are not certified operational aircraft
performance data.
"""

# ==========================================================
# AIRCRAFT REFERENCE DATA
# ==========================================================

aircrafts = {
    # ======================================================
    # AIRBUS
    # ======================================================
    1: {
        "manufacturer": "Airbus",
        "model": "A220-100",
        "speed": 871,
        "fuel_consumption": 2.1,
        "takeoff_distance": 1800,
        "landing_distance": 1400,
        "reference_weight": 60000,
    },
    2: {
        "manufacturer": "Airbus",
        "model": "A220-300",
        "speed": 871,
        "fuel_consumption": 2.2,
        "takeoff_distance": 1900,
        "landing_distance": 1450,
        "reference_weight": 67000,
    },
    3: {
        "manufacturer": "Airbus",
        "model": "A318",
        "speed": 828,
        "fuel_consumption": 2.3,
        "takeoff_distance": 1800,
        "landing_distance": 1350,
        "reference_weight": 59000,
    },
    4: {
        "manufacturer": "Airbus",
        "model": "A319",
        "speed": 828,
        "fuel_consumption": 2.4,
        "takeoff_distance": 1950,
        "landing_distance": 1450,
        "reference_weight": 62500,
    },
    5: {
        "manufacturer": "Airbus",
        "model": "A320",
        "speed": 828,
        "fuel_consumption": 2.5,
        "takeoff_distance": 2100,
        "landing_distance": 1500,
        "reference_weight": 64500,
    },
    6: {
        "manufacturer": "Airbus",
        "model": "A320neo",
        "speed": 830,
        "fuel_consumption": 2.4,
        "takeoff_distance": 2050,
        "landing_distance": 1500,
        "reference_weight": 73500,
    },
    7: {
        "manufacturer": "Airbus",
        "model": "A321",
        "speed": 833,
        "fuel_consumption": 2.8,
        "takeoff_distance": 2200,
        "landing_distance": 1600,
        "reference_weight": 76500,
    },
    8: {
        "manufacturer": "Airbus",
        "model": "A321neo",
        "speed": 833,
        "fuel_consumption": 2.7,
        "takeoff_distance": 2200,
        "landing_distance": 1600,
        "reference_weight": 79000,
    },
    9: {
        "manufacturer": "Airbus",
        "model": "A330-200",
        "speed": 871,
        "fuel_consumption": 4.8,
        "takeoff_distance": 2500,
        "landing_distance": 1800,
        "reference_weight": 230000,
    },
    10: {
        "manufacturer": "Airbus",
        "model": "A330-300",
        "speed": 871,
        "fuel_consumption": 5.0,
        "takeoff_distance": 2600,
        "landing_distance": 1850,
        "reference_weight": 240000,
    },
    11: {
        "manufacturer": "Airbus",
        "model": "A330neo",
        "speed": 880,
        "fuel_consumption": 4.7,
        "takeoff_distance": 2600,
        "landing_distance": 1850,
        "reference_weight": 240000,
    },
    12: {
        "manufacturer": "Airbus",
        "model": "A340-300",
        "speed": 881,
        "fuel_consumption": 5.8,
        "takeoff_distance": 2800,
        "landing_distance": 1900,
        "reference_weight": 240000,
    },
    13: {
        "manufacturer": "Airbus",
        "model": "A340-600",
        "speed": 881,
        "fuel_consumption": 6.3,
        "takeoff_distance": 2900,
        "landing_distance": 2000,
        "reference_weight": 275000,
    },
    14: {
        "manufacturer": "Airbus",
        "model": "A350-900",
        "speed": 903,
        "fuel_consumption": 5.3,
        "takeoff_distance": 2600,
        "landing_distance": 1800,
        "reference_weight": 220000,
    },
    15: {
        "manufacturer": "Airbus",
        "model": "A350-1000",
        "speed": 903,
        "fuel_consumption": 5.7,
        "takeoff_distance": 2800,
        "landing_distance": 1900,
        "reference_weight": 245000,
    },
    16: {
        "manufacturer": "Airbus",
        "model": "A380-800",
        "speed": 903,
        "fuel_consumption": 9.5,
        "takeoff_distance": 3000,
        "landing_distance": 2000,
        "reference_weight": 450000,
    },
    # ======================================================
    # BOEING
    # ======================================================
    17: {
        "manufacturer": "Boeing",
        "model": "717",
        "speed": 811,
        "fuel_consumption": 2.2,
        "takeoff_distance": 1900,
        "landing_distance": 1400,
        "reference_weight": 54000,
    },
    18: {
        "manufacturer": "Boeing",
        "model": "727",
        "speed": 907,
        "fuel_consumption": 3.4,
        "takeoff_distance": 2300,
        "landing_distance": 1600,
        "reference_weight": 83000,
    },
    19: {
        "manufacturer": "Boeing",
        "model": "737-700",
        "speed": 828,
        "fuel_consumption": 2.4,
        "takeoff_distance": 2000,
        "landing_distance": 1450,
        "reference_weight": 58000,
    },
    20: {
        "manufacturer": "Boeing",
        "model": "737-800",
        "speed": 842,
        "fuel_consumption": 2.5,
        "takeoff_distance": 2200,
        "landing_distance": 1500,
        "reference_weight": 65000,
    },
    21: {
        "manufacturer": "Boeing",
        "model": "737-900",
        "speed": 842,
        "fuel_consumption": 2.7,
        "takeoff_distance": 2300,
        "landing_distance": 1550,
        "reference_weight": 70000,
    },
    22: {
        "manufacturer": "Boeing",
        "model": "747-400",
        "speed": 907,
        "fuel_consumption": 8.5,
        "takeoff_distance": 3000,
        "landing_distance": 2000,
        "reference_weight": 285000,
    },
    23: {
        "manufacturer": "Boeing",
        "model": "747-8",
        "speed": 908,
        "fuel_consumption": 8.8,
        "takeoff_distance": 3100,
        "landing_distance": 2050,
        "reference_weight": 295000,
    },
    24: {
        "manufacturer": "Boeing",
        "model": "757-200",
        "speed": 850,
        "fuel_consumption": 3.2,
        "takeoff_distance": 2200,
        "landing_distance": 1500,
        "reference_weight": 100000,
    },
    25: {
        "manufacturer": "Boeing",
        "model": "767-300",
        "speed": 851,
        "fuel_consumption": 4.5,
        "takeoff_distance": 2500,
        "landing_distance": 1750,
        "reference_weight": 159000,
    },
    26: {
        "manufacturer": "Boeing",
        "model": "777-200",
        "speed": 905,
        "fuel_consumption": 6.5,
        "takeoff_distance": 2700,
        "landing_distance": 1900,
        "reference_weight": 224000,
    },
    27: {
        "manufacturer": "Boeing",
        "model": "777-300",
        "speed": 905,
        "fuel_consumption": 7.0,
        "takeoff_distance": 2900,
        "landing_distance": 2000,
        "reference_weight": 299000,
    },
    28: {
        "manufacturer": "Boeing",
        "model": "787-8",
        "speed": 903,
        "fuel_consumption": 5.6,
        "takeoff_distance": 2500,
        "landing_distance": 1750,
        "reference_weight": 227000,
    },
    29: {
        "manufacturer": "Boeing",
        "model": "787-9",
        "speed": 903,
        "fuel_consumption": 5.8,
        "takeoff_distance": 2600,
        "landing_distance": 1800,
        "reference_weight": 254000,
    },
    30: {
        "manufacturer": "Boeing",
        "model": "787-10",
        "speed": 903,
        "fuel_consumption": 6.0,
        "takeoff_distance": 2700,
        "landing_distance": 1850,
        "reference_weight": 254000,
    },
}
