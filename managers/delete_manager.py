import csv

from config.config import CSV_FILE

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

    updated_rows = []
    flight_found = False

    with open(CSV_FILE, "r", encoding="utf-8") as file:
        reader = csv.reader(file)

        header = next(reader)
        updated_rows.append(header)

        for row in reader:

            if row[0] == flight_number:
                flight_found = True
                continue

            updated_rows.append(row)

    if not flight_found:
        print("\nFlight not found.")
        return

    with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(updated_rows)

    print("\nFlight deleted successfully.")
