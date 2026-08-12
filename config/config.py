# ==========================================================
# Project
# ==========================================================

PROJECT_TITLE = "AeroFlight Suite"

LINE_SMALL = 60
LINE_MEDIUM = 80
LINE_LARGE = 100
LINE_XLARGE = 120

DATE_FORMAT = "%Y-%m-%d"

DECIMAL_PRECISION = 2

FLIGHT_NUMBER_PATTERN = r"^[A-Z]{2}\d{3,4}$"


# ==========================================================
# Geographic Configuration
# ==========================================================

EARTH_RADIUS_KM = 6371.0

MIN_LATITUDE = -90.0
MAX_LATITUDE = 90.0

MIN_LONGITUDE = -180.0
MAX_LONGITUDE = 180.0


# ==========================================================
# Weather
# ==========================================================

WIND_DIRECTIONS = {
    "1": "Headwind",
    "2": "Tailwind",
    "3": "Crosswind",
}

WEATHER_CONDITIONS = {
    "1": "Clear",
    "2": "Cloudy",
    "3": "Rain",
    "4": "Storm",
}

WEATHER_SEVERITY = (
    "Low",
    "Medium",
    "High",
)


# ==========================================================
# Weather Severity Scoring
# ==========================================================

WEATHER_SCORE_MAJOR = 2
WEATHER_SCORE_MINOR = 1

WEATHER_SEVERITY_HIGH_SCORE = 5
WEATHER_SEVERITY_MEDIUM_SCORE = 3


# ---------------------------------------------------------------------------
# PROJECT PATHS
# ---------------------------------------------------------------------------

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
# DATABASE
# ---------------------------------------------------------------------------

DATABASE_FILE = str(PROJECT_ROOT / "database" / "aeroflight.db")

BACKUP_FOLDER = str(PROJECT_ROOT / "backups")


# ==========================================================
# Flight Defaults
# ==========================================================

DEFAULT_STATUS = "Scheduled"


# ==========================================================
# Flight Status
# ==========================================================

FLIGHT_STATUSES = {
    "1": "Scheduled",
    "2": "Boarding",
    "3": "Departed",
    "4": "Delayed",
    "5": "Cancelled",
    "6": "Landed",
}


# ==========================================================
# UI Titles
# ==========================================================

TITLE_FLIGHT_INFORMATION = "FLIGHT INFORMATION"
TITLE_AVAILABLE_AIRPORTS = "AVAILABLE AIRPORTS"
TITLE_WEATHER_INFORMATION = "WEATHER INFORMATION"
TITLE_FLIGHT_REPORT = "FLIGHT REPORT"

TITLE_AIRCRAFT_SELECTED = "AIRCRAFT SELECTED"

TITLE_AIRCRAFT_DATABASE = "AIRCRAFT DATABASE"
TITLE_AIRPORT_DATABASE = "AIRPORT DATABASE"

TITLE_SEARCH_RESULTS = "SEARCH RESULTS"

TITLE_FLIGHT_HISTORY = "FLIGHT HISTORY"
TITLE_FLIGHT_STATISTICS = "FLIGHT STATISTICS"

TITLE_DATABASE_BACKUP = "DATABASE BACKUP"

TITLE_SORT_RESULTS = "SORT RESULTS"
TITLE_FILTER_RESULTS = "FILTER RESULTS"
TITLE_ADVANCED_SEARCH = "ADVANCED SEARCH"

TITLE_FLIGHT_FILTER = "FLIGHT FILTER"
TITLE_SORT_FLIGHTS = "SORT FLIGHTS"

TITLE_DELETE_FLIGHT = "DELETE FLIGHT"
TITLE_UPDATE_FLIGHT_STATUS = "UPDATE FLIGHT STATUS"


# ==========================================================
# Messages
# ==========================================================

MSG_START_NEW_FLIGHT = "Starting a new flight..."
MSG_INVALID_FLIGHT_NUMBER = "Invalid flight number."
MSG_FLIGHT_ALREADY_EXISTS = "Flight already exists."
MSG_DISTANCE = "Distance"
MSG_WEATHER_INTELLIGENCE = "WEATHER INTELLIGENCE"
MSG_WEATHER_CONDITION = "Weather Condition"
MSG_INVALID_CHOICE = "Invalid choice."
MSG_FLIGHT_SAVED = "Flight saved successfully."

MSG_NO_FLIGHTS_FOUND = "No flights found."

MSG_SEARCH_EMPTY = "Search cannot be empty."
MSG_NO_AIRCRAFT_FOUND = "No aircraft found."
MSG_NO_AIRPORT_FOUND = "No airport found."

MSG_OPERATION_CANCELLED = "Operation cancelled."
MSG_FLIGHT_NOT_FOUND = "Flight not found."
MSG_FLIGHT_DELETED = "Flight deleted successfully."

MSG_AVAILABLE_STATUS = "Available Status:"
MSG_INVALID_STATUS = "Invalid status."
MSG_STATUS_UPDATED = "Flight status updated successfully."

MSG_CONFIRM_DELETE = "Are you sure you want to delete flight"


# ==========================================================
# Prompts
# ==========================================================

PROMPT_SEARCH = "Search (Flight, Aircraft, Route): "
PROMPT_FLIGHT_NUMBER = "Flight Number: "
PROMPT_AIRCRAFT = "Aircraft: "
PROMPT_DEPARTURE = "Departure: "
PROMPT_ARRIVAL = "Arrival: "
PROMPT_VALUE = "Value: "
PROMPT_CHOOSE_OPTION = "Choose option: "
PROMPT_MIN_DISTANCE = "Minimum Distance: "
PROMPT_MIN_WEATHER = "Minimum Weather Factor: "
PROMPT_CHOOSE_STATUS = "Choose Status: "
PROMPT_FUEL_PRICE = "Fuel Price (€/L): "
PROMPT_VISIBILITY = "Visibility (km): "
PROMPT_WEATHER_CHOICE = "Choose: "
PROMPT_DEPARTURE_AIRPORT = "Departure Airport: "

MSG_EXIT = "Thank you for using AeroFlight Suite."
MSG_INVALID_OPTION = "Invalid option. Please try again."

PROMPT_MENU_CHOICE = "Choose an option: "


# ==========================================================
# Menu Labels
# ==========================================================

MENU_SEARCH = "Search"
MENU_RETURN_MAIN = "Return to Main Menu"
MENU_ITEM_AIRCRAFT = "Aircraft"
MENU_ITEM_AIRPORT = "Airport"

MENU_NEW_FLIGHT = "New Flight"
MENU_AIRCRAFT_DATABASE = "Aircraft Database"
MENU_AIRPORT_DATABASE = "Airport Database"
MENU_FLIGHT_HISTORY = "Flight History"
MENU_STATISTICS = "Statistics"
MENU_SEARCH_FLIGHT = "Search Flight"
MENU_ADVANCED_SEARCH = "Advanced Search"
MENU_FILTER_FLIGHTS = "Filter Flights"
MENU_SORT_FLIGHTS = "Sort Flights"
MENU_BACKUP_DATABASE = "Backup Database"
MENU_DELETE_FLIGHT = "Delete Flight"
MENU_UPDATE_STATUS = "Update Flight Status"
MENU_EXIT = "Exit"


# ==========================================================
# Flight Labels
# ==========================================================

LABEL_MANUFACTURER = "Manufacturer"
LABEL_MODEL = "Model"
LABEL_SPEED = "Speed"
LABEL_FUEL_RATE = "Fuel Rate"
LABEL_FLIGHT_NUMBER = "Flight Number"
LABEL_DATE = "Date"
LABEL_AIRCRAFT = "Aircraft"
LABEL_ROUTE = "Route"
LABEL_DISTANCE = "Distance"
LABEL_FLIGHT_TIME = "Flight Time"
LABEL_STATUS = "Status"

LABEL_CONDITION = "Condition"
LABEL_SEVERITY = "Severity"
LABEL_WIND_SPEED = "Wind Speed"
LABEL_WIND_DIRECTION = "Wind Direction"
LABEL_TEMPERATURE = "Temperature"
LABEL_PRESSURE = "Pressure"
LABEL_HUMIDITY = "Humidity"
LABEL_VISIBILITY = "Visibility"
LABEL_WEATHER_FACTOR = "Weather Factor"
LABEL_FUEL_USED = "Fuel Used"
LABEL_FUEL_COST = "Fuel Cost"


# ==========================================================
# Weather Intelligence Configuration
# ==========================================================

HEADWIND_FACTOR = 0.002
TAILWIND_FACTOR = 0.001
CROSSWIND_FACTOR = 0.0005

HOT_TEMPERATURE = 35
COLD_TEMPERATURE = -10

HOT_TEMPERATURE_FACTOR = 0.03
COLD_TEMPERATURE_FACTOR = 0.02

LOW_PRESSURE = 1000
HIGH_PRESSURE = 1035

LOW_PRESSURE_FACTOR = 0.02
HIGH_PRESSURE_FACTOR = -0.005

HIGH_HUMIDITY = 80
HIGH_HUMIDITY_FACTOR = 0.01

LOW_VISIBILITY = 5
LOW_VISIBILITY_FACTOR = 0.03

MIN_WEATHER_FACTOR = 0.80


# ==========================================================
# Weather Input Validation Limits
# ==========================================================

MIN_TEMPERATURE = -90
MAX_TEMPERATURE = 60

MAX_WIND_SPEED = 300

MIN_PRESSURE = 870
MAX_PRESSURE = 1085

MAX_VISIBILITY = 100


# ==========================================================
# Weather Labels
# ==========================================================

HEADWIND = "Headwind"
TAILWIND = "Tailwind"
CROSSWIND = "Crosswind"

SEVERITY_LOW = "Low"
SEVERITY_MEDIUM = "Medium"
SEVERITY_HIGH = "High"

DEFAULT_WEATHER = "Clear"


# ==========================================================
# Weather Dictionary Keys
# ==========================================================

WEATHER_KEY_WIND = "wind"
WEATHER_KEY_TEMPERATURE = "temperature"
WEATHER_KEY_PRESSURE = "pressure"
WEATHER_KEY_HUMIDITY = "humidity"
WEATHER_KEY_VISIBILITY = "visibility"


# ==========================================================
# Weather Impact Thresholds
# ==========================================================

WEATHER_MAJOR_IMPACT = 0.02
WEATHER_MINOR_IMPACT = 0.00


# ==========================================================
# Menu Labels
# ==========================================================

MENU_DEPARTURE = "Departure"
MENU_ARRIVAL = "Arrival"
MENU_AIRCRAFT = "Aircraft"
MENU_DISTANCE = "Distance"
MENU_WEATHER_FACTOR = "Weather Factor"
MENU_STATUS = "Status"

MENU_DATE = "Date"
MENU_FUEL_COST = "Fuel Cost"
MENU_FUEL_CONSUMPTION = "Fuel Consumption"

MENU_BACK = "Back"


# ==========================================================
# Filter Keys
# ==========================================================

FILTER_DEPARTURE = "departure"
FILTER_ARRIVAL = "arrival"
FILTER_AIRCRAFT = "aircraft"

FILTER_DISTANCE = "distance"
FILTER_WEATHER_FACTOR = "weather_factor"
FILTER_STATUS = "status"


# ==========================================================
# Sort Keys
# ==========================================================

SORT_DATE = "date"
SORT_DISTANCE = "distance"
SORT_COST = "cost"
SORT_FUEL = "fuel"
SORT_WEATHER = "weather"
