"""
AeroFlight Suite
Delete Manager

Application-level manager responsible for
user interaction related to flight deletion.

Persistence is delegated to flight_repository.
"""

from config.config import (
    LINE_SMALL,
    TITLE_DELETE_FLIGHT,
    MSG_CONFIRM_DELETE,
    MSG_OPERATION_CANCELLED,
    MSG_FLIGHT_NOT_FOUND,
    MSG_FLIGHT_DELETED,
)

from managers.flight_repository import (
    delete,
)

from utils.display import print_title
from utils.logger import logger
from utils.validation import get_input


def delete_flight():
    """
    Delete a flight using its flight number.
    """

    print_title(
        TITLE_DELETE_FLIGHT,
        LINE_SMALL,
    )

    flight_number = get_input(
        "\nFlight Number: ",
        upper=True,
    )

    confirmation = (
        input(f"{MSG_CONFIRM_DELETE} " f"{flight_number}? (y/n): ").strip().lower()
    )

    if confirmation != "y":
        print(f"\n{MSG_OPERATION_CANCELLED}")

        logger.info(f"Flight deletion cancelled: {flight_number}")

        return

    affected = delete(
        flight_number,
    )

    if affected == 0:
        print(f"\n{MSG_FLIGHT_NOT_FOUND}")

        logger.warning(f"Flight deletion failed - not found: " f"{flight_number}")

        return

    print(f"\n{MSG_FLIGHT_DELETED}")

    logger.info(f"Flight deleted: {flight_number}")
