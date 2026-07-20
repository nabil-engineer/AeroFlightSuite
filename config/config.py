APP_NAME = "AeroFlight Suite"
DEFAULT_STATUS = "Scheduled"
FLIGHT_STATUSES = {
    "1": "Scheduled",
    "2": "Boarding",
    "3": "Delayed",
    "4": "Departed",
    "5": "Arrived",
    "6": "Cancelled",
}
DATABASE_FILE = "data/flights.db"
BACKUP_FOLDER = "backup"

LINE_SMALL = 60
LINE_MEDIUM = 95
LINE_LARGE = 110
LINE_XLARGE = 120

DATE_FORMAT = "%Y-%m-%d"

FLIGHT_NUMBER_PATTERN = r"^[A-Z]{1,3}[0-9]{2,5}$"


PROJECT_TITLE = """
============================================================
                    AeroFlight Suite
           Professional Flight Management System
============================================================
"""
