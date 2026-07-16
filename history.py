import csv

from config import LINE_LARGE, CSV_FILE

def show_history():
    print("\n")
    print("=" * LINE_LARGE)
    print(f"{'FLIGHT HISTORY':^{LINE_LARGE}}")
    print("=" * LINE_LARGE)

    print(
        f"{'Flight':<12}"
        f"{'Date':<14}"
        f"{'Pilot':<15}"
        f"{'Aircraft':<25}"
        f"{'Route':<30}"
        f"{'Status':<12}"
        f"{'Distance':<12}"
        f"{'Cost (€)':<12}"
    )

    print("-" * LINE_LARGE)

    try:

        with open(CSV_FILE, "r", encoding="utf-8") as file:

            reader = csv.reader(file)

            next(reader, None)

            for row in reader:

                flight_number = row[0]
                flight_date = row[1]
                pilot = row[2]
                aircraft = row[3] + " " + row[4]
                route = row[5] + " -> " + row[6]
                distance = row[7]
                fuel_cost = float(row[10])
                status = row[11]

                print(
                    f"{flight_number:<12}"
                    f"{flight_date:<14}"
                    f"{pilot:<15}"
                    f"{aircraft:<25}"
                    f"{route:<30}"
                    f"{status:<12}"
                    f"{distance:<12}"
                    f"{fuel_cost:<12.2f}"
                )

    except FileNotFoundError:

        print("\nNo flight history found.")

    except Exception as error:

        print(f"\nUnexpected error: {error}")

    print("=" * LINE_LARGE)
