import os
import shutil
from datetime import datetime

from config.config import (
    DATABASE_FILE,
    BACKUP_FOLDER,
)


def backup_database():
    """
    Create a backup copy of the SQLite database.
    """

    os.makedirs(BACKUP_FOLDER, exist_ok=True)

    backup_name = (
        f"flights_backup_"
        f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
    )

    backup_path = os.path.join(
        BACKUP_FOLDER,
        backup_name,
    )

    try:
        shutil.copy2(
            DATABASE_FILE,
            backup_path,
        )

        print("\nBackup created successfully.")
        print(f"Location: {backup_path}")

    except Exception as error:
        print("\nBackup failed.")
        print(error)