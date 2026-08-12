"""
AeroFlight Suite
Status Manager

Application-level manager responsible for
user interaction related to flight status updates.

Persistence is delegated to flight_repository.
"""

from config.config import (
    FLIGHT_STATUSES,
    LINE_SMALL,
    TITLE_UPDATE_FLIGHT_STATUS,
    MSG_AVAILABLE_STATUS,
    MSG_INVALID_STATUS,
    MSG_FLIGHT_NOT_FOUND,
    MSG_STATUS_UPDATED,
    PROMPT_CHOOSE_STATUS,
)

from managers.flight_repository import (
    update_status,
)

from utils.display import print_title
from utils.logger import logger
from utils.validation import get_input


def update_flight_status():
    """
    Update the status of an existing flight.

    The workflow is responsible for:
    - collecting the flight number
    - displaying valid statuses
    - validating the selected status
    - delegating persistence to the repository
    - displaying the operation result

    Database access is not performed directly here.
    """

    print_title(
        TITLE_UPDATE_FLIGHT_STATUS,
        LINE_SMALL,
    )

    # ======================================================
    # FLIGHT NUMBER
    # ======================================================

    flight_number = get_input(
        "\nFlight Number: ",
        upper=True,
    )

    if not flight_number:
        print(f"\n{MSG_FLIGHT_NOT_FOUND}")
        return

    # ======================================================
    # AVAILABLE STATUSES
    # ======================================================

    print(f"\n{MSG_AVAILABLE_STATUS}")

    for key, status_name in FLIGHT_STATUSES.items():
        print(f"{key}. {status_name}")

    # ======================================================
    # STATUS SELECTION
    # ======================================================

    choice = input(f"\n{PROMPT_CHOOSE_STATUS}").strip()

    if choice not in FLIGHT_STATUSES:
        print(f"\n{MSG_INVALID_STATUS}")
        return

    new_status = FLIGHT_STATUSES[choice]

    # ======================================================
    # PERSISTENCE
    # ======================================================

    affected = update_status(
        flight_number,
        new_status,
    )

    # ======================================================
    # RESULT
    # ======================================================

    if affected == 0:

        print(f"\n{MSG_FLIGHT_NOT_FOUND}")

        logger.warning("Status update failed - " f"flight not found: {flight_number}")

        return

    print(f"\n{MSG_STATUS_UPDATED}")

    logger.info("Status updated: " f"{flight_number} -> {new_status}")
    