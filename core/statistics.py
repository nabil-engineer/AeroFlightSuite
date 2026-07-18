import csv
from config.config import CSV_FILE, LINE_SMALL

def show_statistics():

    total_flights = 0
    total_distance = 0
    total_flight_time = 0
    total_fuel_needed = 0
    total_fuel_cost = 0

    try:
        with open(CSV_FILE, "r", encoding="utf-8") as file:

            reader = csv.reader(file)

            next(reader, None)

            for row in reader:

                if len(row) < 11:
                    continue

                total_flights += 1

                total_distance += float(row[7])
                total_flight_time += float(row[8])
                total_fuel_needed += float(row[9])
                total_fuel_cost += float(row[10])

    except FileNotFoundError:
        print("\nNo statistics available.")
        return
    except Exception as error:
        print(f"\nUnexpected error: {error}")
        return

    if total_flights > 0:
        average_flight_time = total_flight_time / total_flights
    else:
        average_flight_time = 0

    print("\n" + "=" * LINE_SMALL)
    print(f"{'FLIGHT STATISTICS':^{LINE_SMALL}}")
    print("=" * LINE_SMALL)

    print(f"Total Flights       : {total_flights}")
    print(f"Total Distance      : {total_distance:.2f} km")
    print(f"Total Flight Time   : {total_flight_time:.2f} hours")
    print(f"Average Flight Time : {average_flight_time:.2f} hours")
    print(f"Total Fuel Needed   : {total_fuel_needed:.2f} L")
    print(f"Total Fuel Cost     : {total_fuel_cost:.2f} €")

    print("=" * LINE_SMALL)
