"""
AeroFlight Suite
Database Package

This module re-exports all database operations.
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
)

from .delete_queries import (
    delete_flight_database,
)

from .backup_manager import (
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
    "delete_flight_database",
    "backup_database",
]
