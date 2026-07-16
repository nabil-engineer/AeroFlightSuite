import csv

from config import CSV_FILE


def update_flight_status():
    print("\n======================================")
    print("       UPDATE FLIGHT STATUS")
    print("======================================")

    flight_number = input("\nFlight Number: ").strip()

    print("\nAvailable Status:")

    print("1. Scheduled")
    print("2. Boarding")
    print("3. Delayed")
    print("4. Departed")
    print("5. Arrived")
    print("6. Cancelled")

    choice = input("\nChoose Status: ")

    status_list = {
        "1": "Scheduled",
        "2": "Boarding",
        "3": "Delayed",
        "4": "Departed",
        "5": "Arrived",
        "6": "Cancelled",
    }

    if choice not in status_list:
        print("\nInvalid status.")
        return

    new_status = status_list[choice]

    print(f"\nFlight : {flight_number}")
    print(f"New Status : {new_status}")

    updated_rows = []
    flight_found = False

    with open(CSV_FILE, "r", encoding="utf-8") as file:
       reader = csv.reader(file)

       header = next(reader)
       
       updated_rows.append(header)

       for row in reader:
        print(row)

        if row[0] == flight_number:
            row[11] = new_status
            flight_found = True

        updated_rows.append(row)

        if not flight_found:
          print("\nFlight not found.")
          return
        
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
          writer = csv.writer(file)
          writer.writerows(updated_rows)

        print("\nFlight status updated successfully.")    
