from airport_data import airports


def show_airport_database():

    print("\n" + "=" * 90)
    print(" " * 30 + "AIRPORT DATABASE")
    print("=" * 90)

    print(
        f"{'Code':<10}"
        f"{'Airport':<40}"
        f"{'City':<20}"
        f"{'Country':<20}"
    )

    print("-" * 90)

    for code, airport in airports.items():

        print(
            f"{code:<10}"
            f"{airport['name']:<40}"
            f"{airport['city']:<20}"
            f"{airport['country']:<20}"
        )

    print("=" * 90)


def search_airport():

    keyword = input("\nSearch Airport (Code, City or Name): ").lower()

    print("\n" + "=" * 90)
    print("SEARCH RESULTS")
    print("=" * 90)

    found = False

    for code, airport in airports.items():

        if (
            keyword in code.lower()
            or keyword in airport["name"].lower()
            or keyword in airport["city"].lower()
        ):

            found = True

            print(
                f"{code:<10}"
                f"{airport['name']:<40}"
                f"{airport['city']:<20}"
                f"{airport['country']:<20}"
            )

    if not found:
        print("No airport found.")

    print("=" * 90)
    