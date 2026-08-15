"""
AeroFlight Suite
Runway Reference Data

Static runway reference data used by Version 5.

Architecture
------------

Airport
    ↓
Runway Collection
    ↓
Runway Performance

The structure intentionally supports multiple runways
for a single airport.

Each airport code maps to a list of runway definitions.

This module contains reference data only.

Business calculations belong to services.
Database persistence belongs to repositories/database.
"""

runways = {
    # ======================================================
    # RABAT - SALÉ
    # ======================================================
    "RBA": [
        {
            "runway_id": "04/22",
            "length": 3500,
            "width": None,
            "surface": "Asphalt",
            "elevation": 84,
            "heading": 40,
        },
    ],
    # ======================================================
    # CASABLANCA - MOHAMMED V
    # ======================================================
    "CMN": [
        {
            "runway_id": "17L/35R",
            "length": 3717,
            "width": None,
            "surface": "Asphalt",
            "elevation": 200,
            "heading": 170,
        },
        {
            "runway_id": "17R/35L",
            "length": 3720,
            "width": None,
            "surface": "Asphalt",
            "elevation": 200,
            "heading": 170,
        },
    ],
    # ======================================================
    # TANGIER
    # ======================================================
    "TNG": [
        {
            "runway_id": "07/25",
            "length": 3500,
            "width": None,
            "surface": "Asphalt",
            "elevation": 21,
            "heading": 70,
        },
    ],
    # ======================================================
    # MARRAKESH
    # ======================================================
    "RAK": [
        {
            "runway_id": "10/28",
            "length": 3100,
            "width": None,
            "surface": "Asphalt",
            "elevation": 471,
            "heading": 100,
        },
    ],
    # ======================================================
    # PARIS CHARLES DE GAULLE
    # ======================================================
    "CDG": [
        {
            "runway_id": "08L/26R",
            "length": 2700,
            "width": None,
            "surface": "Asphalt",
            "elevation": 119,
            "heading": 80,
        },
        {
            "runway_id": "08R/26L",
            "length": 2700,
            "width": None,
            "surface": "Asphalt",
            "elevation": 119,
            "heading": 80,
        },
        {
            "runway_id": "09L/27R",
            "length": 2700,
            "width": None,
            "surface": "Asphalt",
            "elevation": 119,
            "heading": 90,
        },
        {
            "runway_id": "09R/27L",
            "length": 2700,
            "width": None,
            "surface": "Asphalt",
            "elevation": 119,
            "heading": 90,
        },
    ],
    # ======================================================
    # PARIS ORLY
    # ======================================================
    "ORY": [
        {
            "runway_id": "06/24",
            "length": 3320,
            "width": None,
            "surface": "Asphalt",
            "elevation": 89,
            "heading": 60,
        },
        {
            "runway_id": "07/25",
            "length": 3650,
            "width": None,
            "surface": "Asphalt",
            "elevation": 89,
            "heading": 70,
        },
    ],
    # ======================================================
    # NICE
    # ======================================================
    "NCE": [
        {
            "runway_id": "04L/22R",
            "length": 2570,
            "width": None,
            "surface": "Asphalt",
            "elevation": 4,
            "heading": 40,
        },
        {
            "runway_id": "04R/22L",
            "length": 2960,
            "width": None,
            "surface": "Asphalt",
            "elevation": 4,
            "heading": 40,
        },
    ],
    # ======================================================
    # LONDON HEATHROW
    # ======================================================
    "LHR": [
        {
            "runway_id": "09L/27R",
            "length": 3902,
            "width": None,
            "surface": "Asphalt",
            "elevation": 25,
            "heading": 90,
        },
        {
            "runway_id": "09R/27L",
            "length": 3660,
            "width": None,
            "surface": "Asphalt",
            "elevation": 25,
            "heading": 90,
        },
    ],
    # ======================================================
    # MADRID
    # ======================================================
    "MAD": [
        {
            "runway_id": "14L/32R",
            "length": 3500,
            "width": None,
            "surface": "Asphalt",
            "elevation": 610,
            "heading": 140,
        },
        {
            "runway_id": "14R/32L",
            "length": 4100,
            "width": None,
            "surface": "Asphalt",
            "elevation": 610,
            "heading": 140,
        },
        {
            "runway_id": "18L/36R",
            "length": 3500,
            "width": None,
            "surface": "Asphalt",
            "elevation": 610,
            "heading": 180,
        },
        {
            "runway_id": "18R/36L",
            "length": 4100,
            "width": None,
            "surface": "Asphalt",
            "elevation": 610,
            "heading": 180,
        },
    ],
    # ======================================================
    # NEW YORK JFK
    # ======================================================
    "JFK": [
        {
            "runway_id": "04L/22R",
            "length": 3682,
            "width": None,
            "surface": "Asphalt",
            "elevation": 4,
            "heading": 40,
        },
        {
            "runway_id": "04R/22L",
            "length": 2560,
            "width": None,
            "surface": "Asphalt",
            "elevation": 4,
            "heading": 40,
        },
        {
            "runway_id": "13L/31R",
            "length": 3048,
            "width": None,
            "surface": "Asphalt",
            "elevation": 4,
            "heading": 130,
        },
        {
            "runway_id": "13R/31L",
            "length": 4423,
            "width": None,
            "surface": "Asphalt",
            "elevation": 4,
            "heading": 130,
        },
    ],
}
