from .read_queries import execute_query


def update_status(flight_number, new_status):
    """
    Update the status of an existing flight.
    Returns the number of affected rows.
    """

    return execute_query(
        """
        UPDATE flights
        SET status = ?
        WHERE flight_number = ?
        """,
        (
            new_status,
            flight_number,
        ),
    )
