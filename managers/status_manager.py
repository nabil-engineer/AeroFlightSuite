from config.config import FLIGHT_STATUSES
from database.database_manager import update_status


def update_flight_status():
    print("\n======================================")
    print("       UPDATE FLIGHT STATUS")
    print("======================================")

    flight_number = input("\nFlight Number: ").strip().upper()

    print("\nAvailable Status:")
    for key, status in FLIGHT_STATUSES.items():
        print(f"{key}. {status}")

    choice = input("\nChoose Status: ")

    if choice not in FLIGHT_STATUSES:
        print("\nInvalid status.")
        return

    affected = update_status(
        flight_number,
        FLIGHT_STATUSES[choice],
    )

    if affected == 0:
        print("\nFlight not found.")
    else:
        print("\nFlight status updated successfully.")
