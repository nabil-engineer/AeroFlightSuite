from core.flight import new_flight
from core.history import show_history
from core.statistics import show_statistics
from managers.status_manager import update_flight_status
from managers.delete_manager import delete_flight
from managers.search_manager import (
    search_flight,
    advanced_flight_search,
    filter_menu,
    sort_menu,
    backup_menu,
)
from core.catalog import (
    show_aircraft_database,
    search_aircraft,
    show_airport_database,
    search_airport,
)
from config.config import APP_NAME, LINE_SMALL
from utils.display import pause

def display_menu_options():

    print("1. New Flight")
    print("2. Aircraft Database")
    print("3. Airport Database")
    print("4. Flight History")
    print("5. Statistics")
    print("6. Search Flight")
    print("7. Advanced Search")
    print("8. Filter Flights")
    print("9. Sort Flights")
    print("10. Backup Database")
    print("11. Update Flight Status")
    print("12. Delete Flight")
    print()
    print("13. Exit")


def show_main_menu():

    print("\n" + "=" * LINE_SMALL)
    print(f"{APP_NAME:^{LINE_SMALL}}")
    print("=" * LINE_SMALL)

    display_menu_options()

    print("=" * LINE_SMALL)


def get_user_choice():
    return input("\nChoose an option: ").strip()



def execute_menu_option(choice):

    menu_actions = {
        "1": new_flight,
        "2": aircraft_database_menu,
        "3": airport_database_menu,
        "4": show_history,
        "5": show_statistics,
        "6": search_flight,
        "7": advanced_flight_search,
        "8": filter_menu,
        "9": sort_menu,
        "10": backup_menu,
        "11": update_flight_status,
        "12": delete_flight,
    }

    action = menu_actions.get(choice)

    if action is None:
        return False

    action()
    return True


def run_menu():
    while True:
        show_main_menu()
        choice = get_user_choice()

        if choice == "13":
            print("\nThank you for using AeroFlight Suite.")
            break

        if execute_menu_option(choice):
            if choice != "10":
                pause()
        else:
            print("\nInvalid option. Please try again.")
            pause()


def aircraft_database_menu():

    while True:

        show_aircraft_database()

        print("\n1. Search Aircraft")
        print("2. Return to Main Menu")

        choice = input("\nChoose an option: ")

        if choice == "1":

            search_aircraft()

            pause()

        elif choice == "2":

            break

        else:

            print("\nInvalid choice.")  

            pause()


def airport_database_menu():

    while True:
        show_airport_database()

        print("\n1. Search Airport")
        print("2. Return to Main Menu")

        choice = input("\nChoose an option: ")

        if choice == "1":
            search_airport()
            pause()

        elif choice == "2":
            break

        else:
            print("\nInvalid choice.")

            pause()
