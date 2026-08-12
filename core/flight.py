"""
AeroFlight Suite
Flight Creation Workflow

Application workflow responsible for collecting
user input and coordinating flight creation.

Business calculations are delegated to services.
Persistence is delegated to managers/repositories.
"""

from config.config import (
    LINE_SMALL,
    WEATHER_CONDITIONS,
    TITLE_AIRCRAFT_SELECTED,
    TITLE_FLIGHT_INFORMATION,
    TITLE_AVAILABLE_AIRPORTS,
    TITLE_WEATHER_INFORMATION,
    TITLE_FLIGHT_REPORT,
    MSG_START_NEW_FLIGHT,
    MSG_INVALID_FLIGHT_NUMBER,
    MSG_FLIGHT_ALREADY_EXISTS,
    MSG_DISTANCE,
    MSG_WEATHER_INTELLIGENCE,
    MSG_WEATHER_CONDITION,
    MSG_INVALID_CHOICE,
    MSG_FLIGHT_SAVED,
    LABEL_MANUFACTURER,
    LABEL_MODEL,
    LABEL_SPEED,
    LABEL_FUEL_RATE,
    LABEL_FLIGHT_NUMBER,
    LABEL_DATE,
    LABEL_AIRCRAFT,
    LABEL_ROUTE,
    LABEL_DISTANCE,
    LABEL_FLIGHT_TIME,
    LABEL_STATUS,
    LABEL_CONDITION,
    LABEL_SEVERITY,
    LABEL_WIND_SPEED,
    LABEL_WIND_DIRECTION,
    LABEL_TEMPERATURE,
    LABEL_PRESSURE,
    LABEL_HUMIDITY,
    LABEL_VISIBILITY,
    LABEL_WEATHER_FACTOR,
    LABEL_FUEL_USED,
    LABEL_FUEL_COST,
    PROMPT_FUEL_PRICE,
    PROMPT_WEATHER_CHOICE,
    PROMPT_DEPARTURE_AIRPORT,
)

from data.aircraft_data import aircrafts
from data.airport_data import airports

from managers.flight_manager import (
    flight_exists,
    create_flight,
)
from models.flight_model import Flight

from services.flight_service import (
    FlightService,
)

from services.weather_service import (
    create_weather,
)

from utils.display import (
    print_title,
)

from utils.route_calculator import (
    calculate_distance,
)

from utils.validation import (
    get_aircraft_choice,
    get_airport_code,
    get_arrival_airport,
    get_flight_date,
    get_positive_number,
    get_temperature,
    get_wind_speed,
    get_wind_direction,
    get_pressure,
    get_humidity,
    validate_flight_number,
    get_visibility,
)

# ==========================================================
# Aircraft
# ==========================================================


def select_aircraft():
    """
    Ask the user to select an aircraft.
    """

    return aircrafts[
        get_aircraft_choice(
            aircrafts,
        )
    ]


def display_aircraft_information(aircraft):
    """
    Display selected aircraft information.
    """

    print_title(
        TITLE_AIRCRAFT_SELECTED,
        LINE_SMALL,
    )

    print(f"{LABEL_MANUFACTURER:<13}: " f"{aircraft['manufacturer']}")

    print(f"{LABEL_MODEL:<13}: " f"{aircraft['model']}")

    print(f"{LABEL_SPEED:<13}: " f"{aircraft['speed']} km/h")

    print(f"{LABEL_FUEL_RATE:<13}: " f"{aircraft['fuel_consumption']}")


# ==========================================================
# New Flight Workflow
# ==========================================================


def new_flight():
    """
    Execute the complete flight creation workflow.
    """

    print(f"\n{MSG_START_NEW_FLIGHT}\n")

    aircraft = select_aircraft()

    display_aircraft_information(
        aircraft,
    )

    flight = build_flight(
        aircraft,
    )

    finalize_flight(
        flight,
    )


# ==========================================================
# Flight Construction
# ==========================================================


def build_flight(aircraft):
    """
    Collect flight information and create
    a complete Flight object.
    """

    flight_number, flight_date = get_flight_details()

    pilot = get_pilot()

    departure, arrival, distance = get_route_information()

    weather = get_weather_information()

    fuel_price = get_positive_number(f"\n{PROMPT_FUEL_PRICE}")

    flight_service = FlightService()

    return flight_service.create_flight(
        flight_number=flight_number,
        flight_date=flight_date,
        pilot=pilot,
        aircraft=aircraft,
        departure_code=departure["code"],
        departure_city=departure["city"],
        arrival_code=arrival["code"],
        arrival_city=arrival["city"],
        distance=distance,
        fuel_price=fuel_price,
        weather=weather,
    )


# ==========================================================
# Flight Details
# ==========================================================


def get_flight_details():
    """
    Collect and validate flight number and date.
    """

    print_title(
        TITLE_FLIGHT_INFORMATION,
        LINE_SMALL,
    )

    while True:

        flight_number = input("Flight Number: ").strip().upper()

        if not validate_flight_number(
            flight_number,
        ):
            print(MSG_INVALID_FLIGHT_NUMBER)
            continue

        if flight_exists(
            flight_number,
        ):
            print(MSG_FLIGHT_ALREADY_EXISTS)
            continue

        break

    flight_date = get_flight_date()

    return (
        flight_number,
        flight_date,
    )


def get_pilot():
    """
    Collect the pilot name.

    Pilot is part of the Flight model and database
    schema, therefore the creation workflow must
    collect it instead of silently storing None.
    """

    while True:

        pilot = input("\nPilot: ").strip()

        if pilot:
            return pilot

        print("Pilot name cannot be empty.")


# ==========================================================
# Route
# ==========================================================


def get_route_information():
    """
    Collect airports and calculate route distance.
    """

    print_title(
        TITLE_AVAILABLE_AIRPORTS,
        LINE_SMALL,
    )

    for code, airport in airports.items():

        print(f"{code} - " f"{airport['city']}")

    departure_code = get_airport_code(
        airports,
        PROMPT_DEPARTURE_AIRPORT,
    )

    arrival_code = get_arrival_airport(
        airports,
        departure_code,
    )

    departure = {
        "code": departure_code,
        "city": airports[departure_code]["city"],
    }

    arrival = {
        "code": arrival_code,
        "city": airports[arrival_code]["city"],
    }

    distance = calculate_distance(
        airports[departure_code]["latitude"],
        airports[departure_code]["longitude"],
        airports[arrival_code]["latitude"],
        airports[arrival_code]["longitude"],
    )

    print(f"{MSG_DISTANCE} : " f"{distance:.2f} km")

    return (
        departure,
        arrival,
        distance,
    )


# ==========================================================
# Weather
# ==========================================================


def get_weather_information():
    """
    Collect weather information and create
    a Weather object through weather_service.
    """

    print_title(
        TITLE_WEATHER_INFORMATION,
        LINE_SMALL,
    )

    temperature = get_temperature()

    wind_speed = get_wind_speed()

    wind_direction = get_wind_direction()

    pressure = get_pressure()

    humidity = get_humidity()

    visibility = get_visibility()

    print(f"\n{MSG_WEATHER_CONDITION}")

    for key, value in WEATHER_CONDITIONS.items():

        print(f"{key}. {value}")

    while True:

        choice = input(PROMPT_WEATHER_CHOICE).strip()

        if choice in WEATHER_CONDITIONS:

            condition = WEATHER_CONDITIONS[choice]

            break

        print(MSG_INVALID_CHOICE)

    return create_weather(
        temperature=temperature,
        wind_speed=wind_speed,
        wind_direction=wind_direction,
        pressure=pressure,
        humidity=humidity,
        visibility=visibility,
        condition=condition,
    )


# ==========================================================
# Finalization
# ==========================================================


def finalize_flight(flight):
    """
    Display and persist a completed Flight.
    """

    if not isinstance(
        flight,
        Flight,
    ):
        raise ValueError("A valid Flight object is required.")

    print_report(
        flight,
    )

    save_flight_record(
        flight,
    )


def save_flight_record(flight):
    """
    Persist the flight through the application manager.
    """

    create_flight(
        flight,
    )

    print(f"\n{MSG_FLIGHT_SAVED}")


# ==========================================================
# Flight Report
# ==========================================================


def print_report(flight):
    """
    Display the complete flight report.

    Weather information is obtained through
    Flight.weather_data() instead of accessing
    the Weather object directly.
    """

    print_title(
        TITLE_FLIGHT_REPORT,
        LINE_SMALL,
    )

    weather = flight.weather_data()

    print(f"{LABEL_FLIGHT_NUMBER:<16}: " f"{flight.flight_number}")

    print(f"{LABEL_DATE:<16}: " f"{flight.flight_date}")

    print(f"{'Pilot':<16}: " f"{flight.pilot or 'N/A'}")

    print(f"{LABEL_AIRCRAFT:<16}: " f"{flight.aircraft}")

    print(f"{LABEL_ROUTE:<16}: " f"{flight.route}")

    print(f"{LABEL_DISTANCE:<16}: " f"{flight.distance:.2f} km")

    print(f"{LABEL_FLIGHT_TIME:<16}: " f"{flight.flight_time:.2f} h")

    print(f"{LABEL_STATUS:<16}: " f"{flight.status}")

    print("-" * LINE_SMALL)

    print(MSG_WEATHER_INTELLIGENCE)

    print(f"{LABEL_CONDITION:<16}: " f"{weather['condition']}")

    print(f"{LABEL_SEVERITY:<16}: " f"{weather['severity']}")

    print(f"{LABEL_WIND_SPEED:<16}: " f"{weather['wind_speed']:.2f} km/h")

    print(f"{LABEL_WIND_DIRECTION:<16}: " f"{weather['wind_direction']}")

    print(f"{LABEL_TEMPERATURE:<16}: " f"{weather['temperature']:.2f} °C")

    print(f"{LABEL_PRESSURE:<16}: " f"{weather['pressure']:.2f} hPa")

    print(f"{LABEL_HUMIDITY:<16}: " f"{weather['humidity']:.2f}%")

    print(f"{LABEL_VISIBILITY:<16}: " f"{weather['visibility']:.2f} km")

    print(f"{LABEL_WEATHER_FACTOR:<16}: " f"{flight.weather_factor:.3f}")

    print(f"{LABEL_FUEL_USED:<16}: " f"{flight.fuel_needed:.2f}")

    print(f"{LABEL_FUEL_COST:<16}: " f"{flight.fuel_cost:.2f}")
