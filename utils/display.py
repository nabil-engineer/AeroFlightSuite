"""
AeroFlight Suite
Display Utilities

Centralized console display functions for:

- Flights
- Aircraft
- Airports
- Menus
- Messages

The display layer accepts data coming from different
application layers without depending on SQLite-specific
implementation details.
"""

from config.config import (
    LINE_SMALL,
)

# ==========================================================
# GENERAL DISPLAY
# ==========================================================


def print_title(title, width=LINE_SMALL):
    """
    Print a centered title surrounded by '=' characters.
    """

    print("\n" + "=" * width)
    print(f"{title:^{width}}")
    print("=" * width)


def print_separator(width=LINE_SMALL, character="-"):
    """
    Print a horizontal separator line.
    """

    print(character * width)


def print_table_header(headers, widths):
    """
    Print a formatted table header.

    Parameters
    ----------
    headers : list[str]
        Column titles.

    widths : list[int]
        Width of each column.
    """

    if len(headers) != len(widths):
        raise ValueError("headers and widths must have the same length.")

    row = "".join(f"{str(header):<{width}}" for header, width in zip(headers, widths))

    print(row)


def pause():
    """
    Pause the program until the user presses Enter.
    """

    input("\nPress Enter to continue...")


# ==========================================================
# GENERIC VALUE NORMALIZATION
# ==========================================================


def _get_flight_value(
    flight,
    field,
    default="",
):
    """
    Safely retrieve a field from a flight record.

    Supported record types:

    - sqlite3.Row
    - dict
    - Flight-like objects

    The display layer therefore does not depend on
    one specific persistence representation.
    """

    if flight is None:
        return default

    # ------------------------------------------------------
    # Dictionary / sqlite3.Row style access
    # ------------------------------------------------------

    try:
        value = flight[field]

        if value is not None:
            return value

    except (
        KeyError,
        IndexError,
        TypeError,
    ):
        pass

    # ------------------------------------------------------
    # Object attribute access
    # ------------------------------------------------------

    try:
        value = getattr(
            flight,
            field,
        )

        if value is not None:
            return value

    except AttributeError:
        pass

    return default


def _safe_text(
    value,
    default="N/A",
):
    """
    Convert a value safely to display text.
    """

    if value is None:
        return default

    text = str(value).strip()

    return text if text else default


# ==========================================================
# AIRCRAFT FORMATTING
# ==========================================================


def _format_aircraft(flight):
    """
    Return a readable aircraft name.

    Priority:

    1. aircraft
    2. manufacturer + model
    3. N/A
    """

    aircraft = _safe_text(
        _get_flight_value(
            flight,
            "aircraft",
            "",
        ),
        default="",
    )

    if aircraft:
        return aircraft

    manufacturer = _safe_text(
        _get_flight_value(
            flight,
            "manufacturer",
            "",
        ),
        default="",
    )

    model = _safe_text(
        _get_flight_value(
            flight,
            "model",
            "",
        ),
        default="",
    )

    combined = " ".join(
        part
        for part in (
            manufacturer,
            model,
        )
        if part
    ).strip()

    return combined if combined else "N/A"


# ==========================================================
# ROUTE FORMATTING
# ==========================================================


def _format_airport(
    code,
    city,
):
    """
    Format an airport as:

        CODE - City

    Examples
    --------
    RBA + Rabat
        -> RBA - Rabat

    RBA + empty city
        -> RBA

    empty code + Rabat
        -> Rabat
    """

    normalized_code = str(code).strip() if code is not None else ""

    normalized_city = str(city).strip() if city is not None else ""

    if normalized_code and normalized_city:
        return f"{normalized_code} - " f"{normalized_city}"

    if normalized_code:
        return normalized_code

    if normalized_city:
        return normalized_city

    return ""


def _format_route(flight):
    """
    Build a readable departure -> arrival route.

    The function supports both:

        departure / arrival

    and:

        departure_code / departure_city
        arrival_code / arrival_city
    """

    # ------------------------------------------------------
    # First use the canonical legacy-compatible fields.
    # ------------------------------------------------------

    departure = _get_flight_value(
        flight,
        "departure",
        "",
    )

    arrival = _get_flight_value(
        flight,
        "arrival",
        "",
    )

    departure = str(departure).strip() if departure is not None else ""

    arrival = str(arrival).strip() if arrival is not None else ""

    # ------------------------------------------------------
    # If route fields are unavailable, construct them from
    # normalized airport fields.
    # ------------------------------------------------------

    if not departure:

        departure = _format_airport(
            _get_flight_value(
                flight,
                "departure_code",
                "",
            ),
            _get_flight_value(
                flight,
                "departure_city",
                "",
            ),
        )

    if not arrival:

        arrival = _format_airport(
            _get_flight_value(
                flight,
                "arrival_code",
                "",
            ),
            _get_flight_value(
                flight,
                "arrival_city",
                "",
            ),
        )

    # ------------------------------------------------------
    # Convert "CODE - City" into "City" for the compact
    # history table.
    # ------------------------------------------------------

    if " - " in departure:

        departure = departure.split(
            " - ",
            1,
        )[1].strip()

    if " - " in arrival:

        arrival = arrival.split(
            " - ",
            1,
        )[1].strip()

    if departure and arrival:

        return f"{departure} -> {arrival}"

    if departure:

        return departure

    if arrival:

        return arrival

    return "N/A"


# ==========================================================
# WEATHER FORMATTING
# ==========================================================


def _format_weather(flight):
    """
    Return the weather factor in a compact form.

    Example:

        1.220
    """

    weather_factor = _get_flight_value(
        flight,
        "weather_factor",
        1.0,
    )

    try:

        return f"{float(weather_factor):.3f}"

    except (
        TypeError,
        ValueError,
    ):

        return "N/A"


# ==========================================================
# FLIGHT TABLE
# ==========================================================


def display_flights_table(flights):
    """
    Display flight records in a consistent formatted table.

    Supported records:

    - sqlite3.Row
    - dictionaries
    - Flight-like objects

    Used by:

    - Flight History
    - Global Search
    - Advanced Search
    - Filter Results
    - Sort Results
    """

    # ------------------------------------------------------
    # Normalize the collection
    # ------------------------------------------------------

    if flights is None:

        print("\nNo flights found.")

        return

    try:
        flights = list(flights)

    except TypeError:

        print("\nNo flights found.")

        return

    if not flights:

        print("\nNo flights found.")

        return

    # ------------------------------------------------------
    # Table configuration
    # ------------------------------------------------------

    headers = [
        "Flight",
        "Date",
        "Pilot",
        "Aircraft",
        "Route",
        "Distance",
        "Weather",
    ]

    widths = [
        12,
        14,
        16,
        26,
        24,
        13,
        12,
    ]

    table_width = sum(widths)

    # ------------------------------------------------------
    # Top separator
    # ------------------------------------------------------

    print_separator(
        table_width,
        "=",
    )

    # ------------------------------------------------------
    # Header
    # ------------------------------------------------------

    print_table_header(
        headers,
        widths,
    )

    # ------------------------------------------------------
    # Header separator
    # ------------------------------------------------------

    print_separator(
        table_width,
        "=",
    )

    # ------------------------------------------------------
    # Rows
    # ------------------------------------------------------

    for flight in flights:

        # --------------------------------------------------
        # Flight number
        # --------------------------------------------------

        flight_number = _safe_text(
            _get_flight_value(
                flight,
                "flight_number",
                "",
            )
        )

        # --------------------------------------------------
        # Date
        # --------------------------------------------------

        flight_date = _safe_text(
            _get_flight_value(
                flight,
                "flight_date",
                "",
            )
        )

        # --------------------------------------------------
        # Pilot
        # --------------------------------------------------

        pilot = _safe_text(
            _get_flight_value(
                flight,
                "pilot",
                "",
            )
        )

        # --------------------------------------------------
        # Aircraft
        # --------------------------------------------------

        aircraft = _format_aircraft(
            flight,
        )

        # --------------------------------------------------
        # Route
        # --------------------------------------------------

        route = _format_route(
            flight,
        )

        # --------------------------------------------------
        # Distance
        # --------------------------------------------------

        distance = _get_flight_value(
            flight,
            "distance",
            None,
        )

        try:

            distance_display = f"{float(distance):.2f}"

        except (
            TypeError,
            ValueError,
        ):

            distance_display = "N/A"

        # --------------------------------------------------
        # Weather
        # --------------------------------------------------

        weather_display = _format_weather(
            flight,
        )

        # --------------------------------------------------
        # Row
        # --------------------------------------------------

        print(
            f"{flight_number:<12}"
            f"{flight_date:<14}"
            f"{pilot:<16}"
            f"{aircraft:<26}"
            f"{route:<24}"
            f"{distance_display:<13}"
            f"{weather_display:<12}"
        )

    # ------------------------------------------------------
    # Bottom separator
    # ------------------------------------------------------

    print_separator(
        table_width,
        "=",
    )


# ==========================================================
# AIRCRAFT DISPLAY
# ==========================================================


def display_aircraft_table(aircrafts):
    """
    Display the aircraft database in a formatted table.
    """

    print_table_header(
        [
            "No",
            "Manufacturer",
            "Model",
            "Speed",
            "Fuel(L/km)",
        ],
        [
            5,
            20,
            25,
            15,
            15,
        ],
    )

    print_separator(
        80,
    )

    for number, aircraft in aircrafts.items():

        print(
            f"{number:<5}"
            f"{aircraft['manufacturer']:<20}"
            f"{aircraft['model']:<25}"
            f"{aircraft['speed']:<15}"
            f"{aircraft['fuel_consumption']:<15}"
        )


# ==========================================================
# AIRPORT DISPLAY
# ==========================================================


def display_airport_table(airports):
    """
    Display the airport database in a formatted table.
    """

    print_table_header(
        [
            "Code",
            "Airport",
            "City",
            "Country",
        ],
        [
            8,
            40,
            20,
            20,
        ],
    )

    print_separator(
        95,
    )

    for code, airport in airports.items():

        print(
            f"{code:<8}"
            f"{airport['name']:<40}"
            f"{airport['city']:<20}"
            f"{airport['country']:<20}"
        )


# ==========================================================
# MENU DISPLAY
# ==========================================================


def print_menu(options):
    """
    Print a numbered menu from a dictionary.
    """

    for key, value in options.items():

        print(f"{key}. {value}")


# ==========================================================
# MESSAGES
# ==========================================================


def show_success(message):
    """
    Display a success message.
    """

    print(f"\n[SUCCESS] {message}")
