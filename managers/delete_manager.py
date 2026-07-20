from database.database_manager import delete_flight_database


def delete_flight():

    print("\n======================================")
    print("         DELETE FLIGHT")
    print("======================================")

    flight_number = input("\nFlight Number: ").strip()

    confirmation = input(
        f"Are you sure you want to delete flight {flight_number}? (y/n): "
    ).lower()

    if confirmation != "y":
        print("\nOperation cancelled.")
        return

    affected = delete_flight_database(flight_number)

    if affected == 0:
        print("\nFlight not found.")
    else:
        print("\nFlight deleted successfully.")
