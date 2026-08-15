"""
AeroFlight Suite
Flight Creation Workflow

Version 5.0

Application workflow responsible for collecting user input
and coordinating flight creation.

Business calculations are delegated to services.
Persistence is delegated to managers/repositories.
Runway reference lookup is delegated to runway_repository.
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

from managers.runway_repository import (
    get_runways,
)

from models.flight_model import Flight

from services.flight_service import FlightService

from services.weather_service import create_weather

from utils.display import print_title

from utils.route_calculator import calculate_distance

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
# AIRCRAFT
# ==========================================================


def select_aircraft():
    """Ask the user to select an aircraft."""

    return aircrafts[get_aircraft_choice(aircrafts)]


def display_aircraft_information(aircraft):
    """Display selected aircraft information."""

    print_title(
        TITLE_AIRCRAFT_SELECTED,
        LINE_SMALL,
    )

    print(f"{LABEL_MANUFACTURER:<13}: " f"{aircraft['manufacturer']}")

    print(f"{LABEL_MODEL:<13}: " f"{aircraft['model']}")

    print(f"{LABEL_SPEED:<13}: " f"{aircraft['speed']} km/h")

    fuel_rate = aircraft.get(
        "fuel_rate",
        aircraft.get("fuel_consumption"),
    )

    print(f"{LABEL_FUEL_RATE:<13}: " f"{fuel_rate}")

    if aircraft.get("takeoff_distance") is not None:

        print(f"{'Takeoff Distance':<13}: " f"{aircraft['takeoff_distance']} m")

    if aircraft.get("landing_distance") is not None:

        print(f"{'Landing Distance':<13}: " f"{aircraft['landing_distance']} m")

    if aircraft.get("reference_weight") is not None:

        print(f"{'Reference Weight':<13}: " f"{aircraft['reference_weight']} kg")


# ==========================================================
# NEW FLIGHT WORKFLOW
# ==========================================================


def new_flight():
    """Execute the complete flight creation workflow."""

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
# FLIGHT CONSTRUCTION
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

    runway, aircraft_weight = get_runway_information(
        departure_code=departure["code"],
        aircraft=aircraft,
    )

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
        runway=runway,
        aircraft_weight=aircraft_weight,
        reference_weight=aircraft.get("reference_weight"),
        temperature=(weather.temperature if weather is not None else 15.0),
    )


# ==========================================================
# FLIGHT DETAILS
# ==========================================================


def get_flight_details():
    """Collect and validate flight number and date."""

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
    """Collect the pilot name."""

    while True:

        pilot = input("\nPilot: ").strip()

        if pilot:
            return pilot

        print("Pilot name cannot be empty.")


# ==========================================================
# ROUTE
# ==========================================================


def get_route_information():
    """Collect airports and calculate route distance."""

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
# WEATHER
# ==========================================================


def get_weather_information():
    """Collect weather information and create a Weather object."""

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
# VERSION 5 - RUNWAY WORKFLOW
# ==========================================================


def get_runway_information(
    departure_code,
    aircraft,
):
    """
    Select a departure runway and collect actual aircraft weight.

    Runway performance is optional for compatibility with airports
    that do not yet have reference runway data.

    Returns
    -------
    tuple
        ``(runway, aircraft_weight)``.

        Both values are ``None`` when the selected airport
        has no runway reference data.
    """

    available_runways = get_runways(departure_code)

    if not available_runways:

        print(
            "\nNo runway reference data is "
            f"available for "
            f"{str(departure_code).strip().upper()}."
        )

        print("Runway performance will be " "skipped for this flight.")

        return (
            None,
            None,
        )

    print("\nRUNWAY PERFORMANCE")

    print("-" * LINE_SMALL)

    for index, runway in enumerate(
        available_runways,
        start=1,
    ):

        print(
            f"{index}. "
            f"{runway.runway_id} | "
            f"Length: {runway.length} m | "
            f"Surface: {runway.surface} | "
            f"Elevation: {runway.elevation} m"
        )

    while True:

        choice = input("Choose runway: ").strip()

        try:

            index = int(choice)

        except ValueError:

            print("Invalid runway choice.")

            continue

        if 1 <= index <= len(available_runways):

            runway = available_runways[index - 1]

            break

        print("Invalid runway choice.")

    reference_weight = aircraft.get("reference_weight")

    if reference_weight is None:

        aircraft_weight = get_positive_number("Aircraft Weight (kg): ")

    else:

        print(f"Reference aircraft weight: " f"{reference_weight} kg")

        aircraft_weight = get_positive_number("Actual Aircraft Weight (kg): ")

    return (
        runway,
        aircraft_weight,
    )


# ==========================================================
# FINALIZATION
# ==========================================================


def finalize_flight(flight):
    """Display and persist a completed Flight."""

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
    """Persist the flight through the application manager."""

    create_flight(
        flight,
    )

    print(f"\n{MSG_FLIGHT_SAVED}")


# ==========================================================
# FLIGHT REPORT
# ==========================================================


def print_report(flight):
    """Display the complete flight report."""

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

    print(f"{LABEL_DISTANCE:<16}: " f"{float(flight.distance):.2f} km")

    print(f"{LABEL_FLIGHT_TIME:<16}: " f"{float(flight.flight_time):.2f} h")

    print(f"{LABEL_STATUS:<16}: " f"{flight.status}")

    print("-" * LINE_SMALL)

    print(MSG_WEATHER_INTELLIGENCE)

    print(f"{LABEL_CONDITION:<16}: " f"{weather['condition']}")

    print(f"{LABEL_SEVERITY:<16}: " f"{weather['severity']}")

    print(f"{LABEL_WIND_SPEED:<16}: " f"{float(weather['wind_speed']):.2f} km/h")

    print(f"{LABEL_WIND_DIRECTION:<16}: " f"{weather['wind_direction']}")

    print(f"{LABEL_TEMPERATURE:<16}: " f"{float(weather['temperature']):.2f} °C")

    print(f"{LABEL_PRESSURE:<16}: " f"{float(weather['pressure']):.2f} hPa")

    print(f"{LABEL_HUMIDITY:<16}: " f"{float(weather['humidity']):.2f}%")

    print(f"{LABEL_VISIBILITY:<16}: " f"{float(weather['visibility']):.2f} km")

    print(f"{LABEL_WEATHER_FACTOR:<16}: " f"{float(flight.weather_factor):.3f}")

    print(f"{LABEL_FUEL_USED:<16}: " f"{float(flight.fuel_needed):.2f}")

    print(f"{LABEL_FUEL_COST:<16}: " f"{float(flight.fuel_cost):.2f}")

    # ======================================================
    # VERSION 5 - RUNWAY PERFORMANCE REPORT
    # ======================================================

    if flight.runway is None:

        print("-" * LINE_SMALL)

        print("RUNWAY PERFORMANCE: N/A")

        return

    print("-" * LINE_SMALL)

    print("RUNWAY PERFORMANCE")

    print(f"{'Airport':<24}: " f"{flight.runway.airport_code}")

    print(f"{'Runway':<24}: " f"{flight.runway.runway_id}")

    print(f"{'Runway Length':<24}: " f"{float(flight.runway.length):.2f} m")

    print(f"{'Runway Surface':<24}: " f"{flight.runway.surface}")

    print(f"{'Runway Elevation':<24}: " f"{float(flight.runway.elevation or 0):.2f} m")

    performance = flight.runway_performance

    if not performance:

        print("Performance report: N/A")

        return

    print(
        f"{'Required Takeoff Distance':<24}: "
        f"{float(performance['required_takeoff_distance']):.2f} m"
    )

    print(f"{'Takeoff Margin':<24}: " f"{float(performance['takeoff_margin']):.2f} m")

    print(f"{'Takeoff Status':<24}: " f"{performance['takeoff_status']}")

    print(
        f"{'Required Landing Distance':<24}: "
        f"{float(performance['required_landing_distance']):.2f} m"
    )

    print(f"{'Landing Margin':<24}: " f"{float(performance['landing_margin']):.2f} m")

    print(f"{'Landing Status':<24}: " f"{performance['landing_status']}")
