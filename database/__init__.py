"""
AeroFlight Suite
Database Package

Re-export the public database API from database_manager.
"""

from .database_manager import (
    create_database,
    insert_flight,
    flight_exists,
    get_all_flights,
    search_flights,
    advanced_search,
    filter_flights,
    sort_flights,
    get_statistics,
    update_status,
    update_weather,
    update_flight_cost,
    update_distance,
    delete_flight_database,
    backup_database,
)

__all__ = [
    "create_database",
    "insert_flight",
    "flight_exists",
    "get_all_flights",
    "search_flights",
    "advanced_search",
    "filter_flights",
    "sort_flights",
    "get_statistics",
    "update_status",
    "update_weather",
    "update_flight_cost",
    "update_distance",
    "delete_flight_database",
    "backup_database",
]
