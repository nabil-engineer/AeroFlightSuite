import csv

from config.config import CSV_FILE, LINE_LARGE

def search_flight():
    print("\n" + "=" * LINE_LARGE)
    print("SEARCH FLIGHT")
    print("=" * LINE_LARGE)

    keyword = input("\nSearch by Flight Number or Pilot Name: ").strip().lower()

    found = False

    try:
        with open(CSV_FILE, "r", encoding="utf-8") as file:
            reader = csv.reader(file)

            next(reader, None)

            print(
                f"\n{'Flight':<12}"
                f"{'Pilot':<15}"
                f"{'Aircraft':<25}"
                f"{'Route':<25}"
            )

            print("-" * LINE_LARGE)

            for row in reader:

                flight_number = row[0]
                pilot = row[2]

                if keyword in flight_number.lower() or keyword in pilot.lower():

                    aircraft = row[3] + " " + row[4]
                    route = row[5] + " -> " + row[6]

                    print(
                        f"{flight_number:<12}"
                        f"{pilot:<15}"
                        f"{aircraft:<25}"
                        f"{route:<25}"
                    )

                    found = True

        if not found:
            print("\nNo flight found.")

    except FileNotFoundError:
        print("\nNo flight history found.")
