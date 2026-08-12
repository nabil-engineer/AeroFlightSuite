"""
AeroFlight Suite
Flight Read and Search Queries.

This module contains all read-only database operations
related to flights, including search, filtering, sorting,
and statistics.
"""

from .common import execute_query

from .queries import (
    GET_ALL_FLIGHTS,
    GET_STATISTICS,
)

# ==========================================================
# GLOBAL SEARCH FIELDS
# ==========================================================

# Text fields searched by the global search.
SEARCH_TEXT_FIELDS = (
    "flight_number",
    "flight_date",
    "pilot",
    "manufacturer",
    "model",
    "aircraft",
    "departure",
    "arrival",
    "departure_code",
    "departure_city",
    "arrival_code",
    "arrival_city",
    "status",
    "wind_direction",
    "weather_condition",
    "weather_severity",
)


# Numeric fields searched by the global search.
#
# Numeric values are converted to TEXT before applying
# the LIKE comparison.
SEARCH_NUMERIC_FIELDS = (
    "distance",
    "flight_time",
    "fuel_cost",
    "wind_speed",
    "temperature",
    "pressure",
    "humidity",
    "visibility",
    "weather_factor",
    "speed",
    "fuel_price",
    "fuel_needed",
)

# Complete list used by the global search.
SEARCH_FIELDS = SEARCH_TEXT_FIELDS + SEARCH_NUMERIC_FIELDS


# ==========================================================
# SEARCH HELPERS
# ==========================================================


def build_like_conditions(fields, keyword):
    """
    Build a reusable SQL LIKE condition and parameter tuple.

    Text fields are searched using case-insensitive partial
    matching.

    Numeric fields are normalized with SQLite printf()
    before applying the LIKE comparison.

    The canonical flight fuel field is ``fuel_needed``.

    ``fuel_consumption`` is kept as a legacy compatibility
    column. When the caller searches ``fuel_needed``, both
    the canonical and legacy values are considered through
    COALESCE() so older records remain searchable.

    Parameters
    ----------
    fields : tuple
        Database columns to search.

    keyword : str
        Search keyword.

    Returns
    -------
    tuple
        SQL condition and parameter tuple.

    Raises
    ------
    ValueError
        If no searchable fields are provided.
    """

    if not fields:
        raise ValueError("At least one search field is required.")

    normalized_keyword = str(keyword).strip().lower()

    like_value = f"%{normalized_keyword}%"

    conditions = []
    parameters = []

    for field in fields:

        # ==================================================
        # CANONICAL FUEL FIELD
        # ==================================================

        if field == "fuel_needed":

            conditions.append("""
                LOWER(
                    COALESCE(
                        printf(
                            '%.6f',
                            COALESCE(
                                fuel_needed,
                                fuel_consumption
                            )
                        ),
                        ''
                    )
                ) LIKE ?
                """)

            parameters.append(like_value)

            continue

        # ==================================================
        # NUMERIC FIELDS
        # ==================================================

        if field in SEARCH_NUMERIC_FIELDS:

            conditions.append(f"""
                LOWER(
                    COALESCE(
                        printf(
                            '%.6f',
                            {field}
                        ),
                        ''
                    )
                ) LIKE ?
                """)

            parameters.append(like_value)

            continue

        # ==================================================
        # TEXT FIELDS
        # ==================================================

        conditions.append(f"""
            LOWER(
                COALESCE(
                    {field},
                    ''
                )
            ) LIKE ?
            """)

        parameters.append(like_value)

    condition = " OR ".join(conditions)

    return (
        condition,
        tuple(parameters),
    )


# ==========================================================
# FLIGHT EXISTENCE
# ==========================================================


def flight_exists(flight_number):
    """
    Return True when a flight number already exists.

    Parameters
    ----------
    flight_number : str
        Flight number to check.

    Returns
    -------
    bool
        True if the flight exists, otherwise False.
    """

    if flight_number is None:
        return False

    normalized_flight_number = str(flight_number).strip().upper()

    if not normalized_flight_number:
        return False

    row = execute_query(
        """
        SELECT 1
        FROM flights
        WHERE
            UPPER(
                TRIM(flight_number)
            ) = ?
        LIMIT 1
        """,
        (normalized_flight_number,),
        fetch_one=True,
    )

    return row is not None


# ==========================================================
# GET ALL FLIGHTS
# ==========================================================


def get_all_flights():
    """
    Return all stored flights, newest first.

    Returns
    -------
    Any
        All flight records.
    """

    return execute_query(
        GET_ALL_FLIGHTS,
        fetch=True,
    )


# ==========================================================
# GLOBAL SEARCH
# ==========================================================


def search_flights(keyword):
    """
    Search flights using the global search keyword.

    The search covers text and numeric flight fields.

    Text fields
    -----------
    - Flight number
    - Flight date
    - Pilot
    - Manufacturer
    - Model
    - Aircraft
    - Departure
    - Arrival
    - Departure code
    - Departure city
    - Arrival code
    - Arrival city
    - Status
    - Wind direction
    - Weather condition
    - Weather severity

    Numeric fields
    --------------
    - Distance
    - Flight time
    - Fuel consumption
    - Fuel cost
    - Wind speed
    - Temperature
    - Pressure
    - Humidity
    - Visibility
    - Weather factor
    - Speed
    - Fuel price
    - Fuel needed

    The search is:

    - case-insensitive
    - partial
    - applied across all configured fields

    Examples
    --------
    Search "Scheduled"
        -> finds flights with Scheduled status.

    Search "Boeing"
        -> finds Boeing aircraft.

    Search "Nabil"
        -> finds flights assigned to pilot Nabil.

    Search "Clear"
        -> finds flights with Clear weather.

    Search "Rabat"
        -> finds flights involving Rabat.

    Search "1.22"
        -> can find a matching weather factor.

    Parameters
    ----------
    keyword : str
        Keyword used for the global search.

    Returns
    -------
    Any
        Matching flight records.
    """

    if keyword is None:
        return []

    normalized_keyword = str(keyword).strip()

    if not normalized_keyword:
        return []

    where_clause, parameters = build_like_conditions(
        SEARCH_FIELDS,
        normalized_keyword,
    )

    return execute_query(
        f"""
        SELECT *
        FROM flights

        WHERE
            {where_clause}

        ORDER BY
            id DESC
        """,
        parameters,
        fetch=True,
    )


# ==========================================================
# ADVANCED SEARCH
# ==========================================================


def advanced_search(
    flight_number="",
    aircraft="",
    departure="",
    arrival="",
):
    """
    Perform an advanced flight search.

    All supplied filters are combined with AND.

    Aircraft searches are performed against the canonical
    manufacturer/model fields as well as the compatibility
    aircraft field.

    Route searches are performed against both the normalized
    airport fields and the compatibility route fields.

    Parameters
    ----------
    flight_number : str, optional
        Flight number filter.

    aircraft : str, optional
        Aircraft/manufacturer/model filter.

    departure : str, optional
        Departure airport/code/city filter.

    arrival : str, optional
        Arrival airport/code/city filter.

    Returns
    -------
    Any
        Matching flight records.
    """

    query = """
        SELECT *
        FROM flights
    """

    conditions = []
    parameters = []

    # ======================================================
    # FLIGHT NUMBER
    # ======================================================

    if flight_number is not None:

        normalized_value = str(flight_number).strip()

        if normalized_value:

            conditions.append("""
                LOWER(
                    COALESCE(
                        flight_number,
                        ''
                    )
                ) LIKE ?
                """)

            parameters.append(f"%{normalized_value.lower()}%")

    # ======================================================
    # AIRCRAFT
    # ======================================================
    #
    # Canonical:
    #   manufacturer
    #   model
    #
    # Compatibility:
    #   aircraft
    #
    # ======================================================

    if aircraft is not None:

        normalized_value = str(aircraft).strip()

        if normalized_value:

            aircraft_condition = """
                (
                    LOWER(
                        COALESCE(
                            aircraft,
                            ''
                        )
                    ) LIKE ?

                    OR LOWER(
                        COALESCE(
                            manufacturer,
                            ''
                        )
                    ) LIKE ?

                    OR LOWER(
                        COALESCE(
                            model,
                            ''
                        )
                    ) LIKE ?
                )
            """

            conditions.append(aircraft_condition)

            aircraft_parameter = f"%{normalized_value.lower()}%"

            parameters.extend(
                (
                    aircraft_parameter,
                    aircraft_parameter,
                    aircraft_parameter,
                )
            )

    # ======================================================
    # DEPARTURE
    # ======================================================
    #
    # Canonical:
    #   departure_code
    #   departure_city
    #
    # Compatibility:
    #   departure
    #
    # ======================================================

    if departure is not None:

        normalized_value = str(departure).strip()

        if normalized_value:

            departure_condition = """
                (
                    LOWER(
                        COALESCE(
                            departure_code,
                            ''
                        )
                    ) LIKE ?

                    OR LOWER(
                        COALESCE(
                            departure_city,
                            ''
                        )
                    ) LIKE ?

                    OR LOWER(
                        COALESCE(
                            departure,
                            ''
                        )
                    ) LIKE ?
                )
            """

            conditions.append(departure_condition)

            departure_parameter = f"%{normalized_value.lower()}%"

            parameters.extend(
                (
                    departure_parameter,
                    departure_parameter,
                    departure_parameter,
                )
            )

    # ======================================================
    # ARRIVAL
    # ======================================================

    if arrival is not None:

        normalized_value = str(arrival).strip()

        if normalized_value:

            arrival_condition = """
                (
                    LOWER(
                        COALESCE(
                            arrival_code,
                            ''
                        )
                    ) LIKE ?

                    OR LOWER(
                        COALESCE(
                            arrival_city,
                            ''
                        )
                    ) LIKE ?

                    OR LOWER(
                        COALESCE(
                            arrival,
                            ''
                        )
                    ) LIKE ?
                )
            """

            conditions.append(arrival_condition)

            arrival_parameter = f"%{normalized_value.lower()}%"

            parameters.extend(
                (
                    arrival_parameter,
                    arrival_parameter,
                    arrival_parameter,
                )
            )

    # ======================================================
    # WHERE
    # ======================================================

    if conditions:

        query += """
            WHERE
        """

        query += "\nAND\n".join(conditions)

    # ======================================================
    # ORDER
    # ======================================================

    query += """
        ORDER BY
            id DESC
    """

    return execute_query(
        query,
        tuple(parameters),
        fetch=True,
    )


# ==========================================================
# FILTER
# ==========================================================


def filter_flights(
    filter_type,
    value,
):
    """
    Filter flights using a supported filter.

    Supported filters
    -----------------
    departure
        Searches departure, departure code,
        or departure city.

    arrival
        Searches arrival, arrival code,
        or arrival city.

    aircraft
        Searches aircraft, manufacturer,
        or model.

    distance
        Returns flights whose distance is greater than
        or equal to the supplied value.

    weather_factor
        Returns flights whose weather factor is greater
        than or equal to the supplied value.

    status
        Searches the flight status using a
        case-insensitive partial match.

    Parameters
    ----------
    filter_type : str
        Supported filter type.

    value : Any
        Value used by the selected filter.

    Returns
    -------
    Any
        Matching flight records.

    Raises
    ------
    ValueError
        If the filter type is not supported or the
        required value is missing.
    """

    if filter_type is None:
        raise ValueError("Filter type is required.")

    normalized_filter = str(filter_type).strip().lower()

    if value is None:
        raise ValueError("Filter value is required.")

    normalized_value = str(value).strip()

    if not normalized_value:
        raise ValueError("Filter value cannot be empty.")

    # ======================================================
    # DEPARTURE
    # ======================================================

    if normalized_filter == "departure":

        search_value = f"%{normalized_value.lower()}%"

        return execute_query(
            """
            SELECT *
            FROM flights

            WHERE
                LOWER(
                    COALESCE(
                        departure,
                        ''
                    )
                ) LIKE ?

                OR LOWER(
                    COALESCE(
                        departure_code,
                        ''
                    )
                ) LIKE ?

                OR LOWER(
                    COALESCE(
                        departure_city,
                        ''
                    )
                ) LIKE ?

            ORDER BY
                id DESC
            """,
            (
                search_value,
                search_value,
                search_value,
            ),
            fetch=True,
        )

    # ======================================================
    # ARRIVAL
    # ======================================================

    if normalized_filter == "arrival":

        search_value = f"%{normalized_value.lower()}%"

        return execute_query(
            """
            SELECT *
            FROM flights

            WHERE
                LOWER(
                    COALESCE(
                        arrival,
                        ''
                    )
                ) LIKE ?

                OR LOWER(
                    COALESCE(
                        arrival_code,
                        ''
                    )
                ) LIKE ?

                OR LOWER(
                    COALESCE(
                        arrival_city,
                        ''
                    )
                ) LIKE ?

            ORDER BY
                id DESC
            """,
            (
                search_value,
                search_value,
                search_value,
            ),
            fetch=True,
        )

    # ======================================================
    # AIRCRAFT
    # ======================================================

    if normalized_filter == "aircraft":

        search_value = f"%{normalized_value.lower()}%"

        return execute_query(
            """
            SELECT *
            FROM flights

            WHERE
                LOWER(
                    COALESCE(
                        aircraft,
                        ''
                    )
                ) LIKE ?

                OR LOWER(
                    COALESCE(
                        manufacturer,
                        ''
                    )
                ) LIKE ?

                OR LOWER(
                    COALESCE(
                        model,
                        ''
                    )
                ) LIKE ?

            ORDER BY
                id DESC
            """,
            (
                search_value,
                search_value,
                search_value,
            ),
            fetch=True,
        )

    # ======================================================
    # DISTANCE
    # ======================================================

    if normalized_filter == "distance":

        try:

            numeric_value = float(normalized_value)

        except (
            TypeError,
            ValueError,
        ) as error:

            raise ValueError("Distance filter requires " "a numeric value.") from error

        return execute_query(
            """
            SELECT *
            FROM flights

            WHERE
                distance >= ?

            ORDER BY
                distance DESC,
                id DESC
            """,
            (numeric_value,),
            fetch=True,
        )

    # ======================================================
    # WEATHER FACTOR
    # ======================================================

    if normalized_filter == "weather_factor":

        try:

            numeric_value = float(normalized_value)

        except (
            TypeError,
            ValueError,
        ) as error:

            raise ValueError(
                "Weather factor filter requires " "a numeric value."
            ) from error

        return execute_query(
            """
            SELECT *
            FROM flights

            WHERE
                weather_factor >= ?

            ORDER BY
                weather_factor DESC,
                id DESC
            """,
            (numeric_value,),
            fetch=True,
        )

    # ======================================================
    # STATUS
    # ======================================================

    if normalized_filter == "status":

        search_value = f"%{normalized_value.lower()}%"

        return execute_query(
            """
            SELECT *
            FROM flights

            WHERE
                LOWER(
                    COALESCE(
                        status,
                        ''
                    )
                ) LIKE ?

            ORDER BY
                id DESC
            """,
            (search_value,),
            fetch=True,
        )

    # ======================================================
    # UNKNOWN FILTER
    # ======================================================

    raise ValueError(f"Unknown filter type: " f"{normalized_filter}")


# ==========================================================
# SORT
# ==========================================================


def sort_flights(order):
    """
    Sort flights using a supported sort option.

    The canonical fuel field used by AeroFlight Suite
    is ``fuel_needed``.

    ``fuel_consumption`` is a legacy compatibility
    column and is intentionally not used for new
    application-level sorting.

    Parameters
    ----------
    order : str
        Supported sort option.

    Supported values
    -----------------
    date
        Newest flight date first.

    distance
        Longest distance first.

    cost
        Highest fuel cost first.

    fuel
        Highest required fuel first.

    weather
        Highest weather factor first.

    Returns
    -------
    list[sqlite3.Row]
        Sorted flight records.

    Raises
    ------
    ValueError
        If the sort option is missing or unsupported.
    """

    if order is None:
        raise ValueError("Sort option is required.")

    normalized_order = str(order).strip().lower()

    queries = {
        # ==================================================
        # DATE
        # ==================================================
        "date": """
            SELECT *
            FROM flights

            ORDER BY
                flight_date DESC,
                id DESC
        """,
        # ==================================================
        # DISTANCE
        # ==================================================
        "distance": """
            SELECT *
            FROM flights

            ORDER BY
                distance DESC,
                id DESC
        """,
        # ==================================================
        # FUEL COST
        # ==================================================
        "cost": """
            SELECT *
            FROM flights

            ORDER BY
                fuel_cost DESC,
                id DESC
        """,
        # ==================================================
        # FUEL NEEDED
        # ==================================================
        "fuel": """
            SELECT *
            FROM flights

            ORDER BY
                COALESCE(
                    fuel_needed,
                    fuel_consumption,
                    0
                ) DESC,
                id DESC
        """,
        # ==================================================
        # WEATHER
        # ==================================================
        "weather": """
            SELECT *
            FROM flights

            ORDER BY
                weather_factor DESC,
                id DESC
        """,
    }

    query = queries.get(normalized_order)

    if query is None:
        raise ValueError(f"Unknown sort option: " f"{normalized_order}")

    return execute_query(
        query,
        fetch=True,
    )


# ==========================================================
# STATISTICS
# ==========================================================


def get_statistics():
    """
    Return aggregate flight statistics.

    Returns
    -------
    Any
        Aggregate flight statistics.
    """

    return execute_query(
        GET_STATISTICS,
        fetch_one=True,
    )
