from aircraft_data import aircrafts


def show_aircraft_database():

    print("\n" + "=" * 95)
    print(" " * 32 + "AIRCRAFT DATABASE")
    print("=" * 95)

    print(
        f"{'No':<5}"
        f"{'Manufacturer':<20}"
        f"{'Model':<25}"
        f"{'Speed':<15}"
        f"{'Fuel(L/km)':<15}"
    )

    print("-" * 95)

    for number, aircraft in aircrafts.items():

        print(
            f"{number:<5}"
            f"{aircraft['manufacturer']:<20}"
            f"{aircraft['model']:<25}"
            f"{aircraft['speed']:<15}"
            f"{aircraft['fuel_consumption']:<15}"
        )

    print("=" * 95)

def search_aircraft():

    keyword = input("\nSearch (Manufacturer or Model): ").lower()

    print("\n" + "=" * 95)
    print("SEARCH RESULTS")
    print("=" * 95)

    found = False

    for number, aircraft in aircrafts.items():

        manufacturer = aircraft["manufacturer"].lower()
        model = aircraft["model"].lower()

        if keyword in manufacturer or keyword in model:

            found = True

            print(
                f"{number:<5}"
                f"{aircraft['manufacturer']:<20}"
                f"{aircraft['model']:<25}"
                f"{aircraft['speed']:<15}"
                f"{aircraft['fuel_consumption']:<15}"
            )

    if not found:

        print("No aircraft found.")

    print("=" * 95)    