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
)

from .read_queries import (
    flight_exists,
    get_all_flights,
    search_flights,
    advanced_search,
    filter_flights,
    sort_flights,
    get_statistics,
)

from .update_queries import (
    update_status,
    update_weather,
    update_flight_cost,
    update_distance,
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
    # Read
    "flight_exists",
    "get_all_flights",
    "search_flights",
    "advanced_search",
    "filter_flights",
    "sort_flights",
    "get_statistics",
    # Update
    "update_status",
    "update_weather",
    "update_flight_cost",
    "update_distance",
    # Delete
    "delete_flight_database",
    # Backup
    "backup_database",
]
