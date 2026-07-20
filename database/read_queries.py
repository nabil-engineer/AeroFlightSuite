from .common import execute_query, execute_single


def flight_exists(flight_number):

    return (
        execute_single(
            """
            SELECT 1
            FROM flights
            WHERE flight_number = ?
            """,
            (flight_number,),
        )
        is not None
    )


def get_all_flights():

    return execute_query(
        """
        SELECT *
        FROM flights
        ORDER BY id DESC
        """,
        fetch=True,
    )


def search_flights(keyword):

    keyword = f"%{keyword.lower()}%"

    fields = (
        "flight_number",
        "pilot",
        "manufacturer",
        "model",
        "departure_city",
        "arrival_city",
        "status",
    )

    where_clause = " OR ".join(f"LOWER({field}) LIKE ?" for field in fields)

    return execute_query(
        f"""
        SELECT *
        FROM flights
        WHERE {where_clause}
        ORDER BY id DESC
        """,
        (keyword,) * len(fields),
        fetch=True,
    )


def advanced_search(
    flight_number="",
    pilot="",
    aircraft="",
    departure="",
    arrival="",
    status="",
):

    query = """
    SELECT *
    FROM flights
    WHERE
        LOWER(flight_number) LIKE ?
        AND LOWER(pilot) LIKE ?
        AND LOWER(manufacturer || ' ' || model) LIKE ?
        AND LOWER(departure_city) LIKE ?
        AND LOWER(arrival_city) LIKE ?
        AND LOWER(status) LIKE ?
    ORDER BY id DESC
    """

    parameters = (
        f"%{flight_number.lower()}%",
        f"%{pilot.lower()}%",
        f"%{aircraft.lower()}%",
        f"%{departure.lower()}%",
        f"%{arrival.lower()}%",
        f"%{status.lower()}%",
    )

    return execute_query(
        query,
        parameters,
        fetch=True,
    )


def filter_flights(filter_type, value):

    queries = {
        "status": (
            "SELECT * FROM flights WHERE status = ? ORDER BY id DESC",
            (value,),
        ),
        "departure": (
            "SELECT * FROM flights WHERE departure_city = ? ORDER BY id DESC",
            (value,),
        ),
        "arrival": (
            "SELECT * FROM flights WHERE arrival_city = ? ORDER BY id DESC",
            (value,),
        ),
        "distance": (
            "SELECT * FROM flights WHERE distance >= ? ORDER BY distance DESC",
            (value,),
        ),
    }

    if filter_type not in queries:
        return []

    query, parameters = queries[filter_type]

    return execute_query(
        query,
        parameters,
        fetch=True,
    )


def sort_flights(order):

    queries = {
        "date": "SELECT * FROM flights ORDER BY flight_date DESC",
        "distance": "SELECT * FROM flights ORDER BY distance DESC",
        "cost": "SELECT * FROM flights ORDER BY fuel_cost DESC",
        "pilot": "SELECT * FROM flights ORDER BY pilot ASC",
    }

    query = queries.get(order)

    if query is None:
        return []

    return execute_query(
        query,
        fetch=True,
    )


def get_statistics():

    return execute_single("""
        SELECT
            COUNT(*),
            SUM(distance),
            SUM(flight_time),
            SUM(fuel_needed),
            SUM(fuel_cost)
        FROM flights
        """)
