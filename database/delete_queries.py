from .read_queries import execute_query


def delete_flight_database(flight_number):
    """
    Delete a flight using its flight number.
    Returns the number of deleted rows.
    """

    return execute_query(
        """
        DELETE
        FROM flights
        WHERE flight_number = ?
        """,
        (flight_number,),
    )
