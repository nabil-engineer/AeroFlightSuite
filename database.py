from aircraft_data import aircrafts
from airport_data import airports
from config import LINE_MEDIUM, LINE_XLARGE

def show_aircraft_database():

    print("\n" + "=" * LINE_MEDIUM)
    print(" " * 32 + "AIRCRAFT DATABASE")
    print("=" * LINE_MEDIUM)

    print(
        f"{'No':<5}"
        f"{'Manufacturer':<20}"
        f"{'Model':<25}"
        f"{'Speed':<15}"
        f"{'Fuel(L/km)':<15}"
    )

    print("-" * LINE_MEDIUM)

    for number, aircraft in aircrafts.items():

        print(
            f"{number:<5}"
            f"{aircraft['manufacturer']:<20}"
            f"{aircraft['model']:<25}"
            f"{aircraft['speed']:<15}"
            f"{aircraft['fuel_consumption']:<15}"
        )

    print("=" * LINE_MEDIUM)

def search_aircraft():

    keyword = input("\nSearch (Manufacturer or Model): ").lower()

    print("=" * LINE_MEDIUM)
    print(f"{'SEARCH RESULTS':^{LINE_MEDIUM}}")
    print("=" * LINE_MEDIUM)

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

    print("=" * LINE_MEDIUM)


def show_airport_database():

    print("\n" + "=" * LINE_XLARGE)
    print(f"{'AIRPORT DATABASE':^{LINE_XLARGE}}")
    print("=" * LINE_XLARGE)

    print(f"{'Code':<8}" f"{'Airport':<35}" f"{'City':<20}" f"{'Country':<20}")

    print("-" * LINE_XLARGE)

    for code, airport in airports.items():

        print(
            f"{code:<8}"
            f"{airport['name']:<40}"
            f"{airport['city']:<20}"
            f"{airport['country']:<20}"
        )
    print("=" * LINE_XLARGE)


def search_airport():
    keyword = input("\nSearch (Code, Airport, City or Country): ").lower()

    print("=" * LINE_MEDIUM)
    print("SEARCH RESULTS")
    print("=" * LINE_MEDIUM)

    found = False

    for code, airport in airports.items():

        if (
            keyword in code.lower()
            or keyword in airport["name"].lower()
            or keyword in airport["city"].lower()
            or keyword in airport["country"].lower()
        ):

            found = True

            print(
                f"{code:<8}"
                f"{airport['name']:<35}"
                f"{airport['city']:<20}"
                f"{airport['country']:<20}"
            )

    if not found:
        print("No airport found.")

    print("=" * LINE_XLARGE)
