import csv


def show_statistics():

    total_flights = 0
    total_distance = 0
    total_flight_time = 0
    total_fuel_needed = 0
    total_fuel_cost = 0

    with open("data/flights.csv", "r", encoding="utf-8") as file:

        reader = csv.reader(file)

        for row in reader:

            total_flights += 1

            total_distance += float(row[5])
            total_flight_time += float(row[6])
            total_fuel_needed += float(row[7])
            total_fuel_cost += float(row[8])

    if total_flights > 0:
        average_flight_time = total_flight_time / total_flights
    else:
        average_flight_time = 0

    print("\n" + "=" * 60)
    print("                 FLIGHT STATISTICS")
    print("=" * 60)

    print(f"Total Flights       : {total_flights}")
    print(f"Total Distance      : {total_distance:.2f} km")
    print(f"Total Flight Time   : {total_flight_time:.2f} hours")
    print(f"Average Flight Time : {average_flight_time:.2f} hours")
    print(f"Total Fuel Needed   : {total_fuel_needed:.2f} L")
    print(f"Total Fuel Cost     : {total_fuel_cost:.2f} €")

    print("=" * 60)