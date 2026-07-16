import csv


import csv

def show_history():
    print("\n")
    print("=" * 110)
    print(" " * 45 + "FLIGHT HISTORY")
    print("=" * 110)

    print(
        f"{'Pilot':<15}"
        f"{'Aircraft':<25}"
        f"{'Route':<30}"
        f"{'Distance':<12}"
        f"{'Cost (€)':<12}"
    )

    print("-" * 110)

    try:

        with open("data/flights.csv", "r", encoding="utf-8") as file:

            reader = csv.reader(file)

            next(reader, None)

            rows = list(reader)

            if not rows:
                print("\nNo flight history available.")

            for row in rows:    

                pilot = row[0]
                aircraft = row[1] + " " + row[2]
                route = row[3] + " -> " + row[4]
                distance = row[5]
                fuel_cost = row[8]

                print(
                    f"{pilot:<15}"
                    f"{aircraft:<25}"
                    f"{route:<30}"
                    f"{distance:<12}"
                    f"{fuel_cost:<12}"
                )

    except FileNotFoundError:

        print("\nNo flight history available.")

    print("=" * 110)