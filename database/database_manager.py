"""
AeroFlight Suite
Database Package
Central database API.

This module exposes the complete public database interface
by combining the specialized query modules.
"""

from .create_queries import (
    create_database,
    insert_flight,
    insert_runway,
)

from .read_queries import (
    flight_exists,
    get_all_flights,
    search_flights,
    advanced_search,
    filter_flights,
    sort_flights,
    get_statistics,
    get_all_runways,
    get_runways,
    get_runway,
    get_runway_performance,
)

from .update_queries import (
    update_status,
    update_weather,
    update_flight_cost,
    update_distance,
    save_runway_performance,
)

from .delete_queries import (
    delete_flight_database,
)

from .backup_manager import (
    backup_database,
)

__all__ = [
    # Create
    "create_database",
    "insert_flight",
    "insert_runway",
    # Read
    "flight_exists",
    "get_all_flights",
    "search_flights",
    "advanced_search",
    "filter_flights",
    "sort_flights",
    "get_statistics",
    "get_all_runways",
    "get_runways",
    "get_runway",
    "get_runway_performance",
    # Update
    "update_status",
    "update_weather",
    "update_flight_cost",
    "update_distance",
    "save_runway_performance",
    # Delete
    "delete_flight_database",
    # Backup
    "backup_database",
]
