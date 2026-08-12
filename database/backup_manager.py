"""
AeroFlight Suite
Database Backup Manager

Responsible for creating safe SQLite database backups
using SQLite's native backup API.
"""

import os
import sqlite3
from datetime import datetime

from config.config import (
    DATABASE_FILE,
    BACKUP_FOLDER,
)

from utils.logger import logger


def backup_database():
    """
    Create a timestamped SQLite database backup.

    The backup is created using SQLite's native Online Backup API
    instead of copying the database file directly.

    Returns
    -------
    str
        Path to the created backup file.

    Raises
    ------
    FileNotFoundError
        If the source database does not exist.

    RuntimeError
        If the SQLite backup operation fails.
    """

    os.makedirs(
        BACKUP_FOLDER,
        exist_ok=True,
    )

    if not os.path.exists(DATABASE_FILE):
        logger.error(
            "Database file not found: %s",
            DATABASE_FILE,
        )

        raise FileNotFoundError(
            DATABASE_FILE,
        )

    backup_name = f"flights_backup_" f"{datetime.now():%Y%m%d_%H%M%S_%f}.db"

    backup_path = os.path.join(
        BACKUP_FOLDER,
        backup_name,
    )

    try:
        source_connection = sqlite3.connect(
            DATABASE_FILE,
        )

        backup_connection = sqlite3.connect(
            backup_path,
        )

        try:
            with backup_connection:
                source_connection.backup(
                    backup_connection,
                )

        finally:
            backup_connection.close()
            source_connection.close()

    except sqlite3.Error as error:
        logger.exception(
            "Database backup failed.",
        )

        if os.path.exists(backup_path):
            try:
                os.remove(backup_path)
            except OSError:
                logger.warning(
                    "Unable to remove incomplete backup: %s",
                    backup_path,
                )

        raise RuntimeError(f"Database backup failed: {error}") from error

    logger.info(
        "Database backup created: %s",
        backup_path,
    )

    return backup_path
