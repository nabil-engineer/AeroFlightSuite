from core.flight import new_flight
from core.history import show_history
from core.statistics import show_statistics
from status_manager import update_flight_status
from delete_manager import delete_flight
from core.database import (
    show_aircraft_database,
    search_aircraft,
    show_airport_database,
    search_airport,
)
from config.config import APP_NAME, LINE_SMALL

def show_main_menu():
    print("\n" + "=" * LINE_SMALL)
    print(f"{APP_NAME:^60}")
    print("=" * LINE_SMALL)
    print("1. New Flight")
    print("2. Aircraft Database")
    print("3. Airport Database")
    print("4. Flight History")
    print("5. Statistics")
    print("6. Update Flight Status")
    print("7. Delete Flight")
    print("8. Exit")
    print("=" * LINE_SMALL)


def run_menu():

    while True:

        show_main_menu()

        menu_choice = input("Choose an option: ")

        if menu_choice == "1":

            new_flight()

        elif menu_choice == "2":

            aircraft_database_menu()

        elif menu_choice == "3":

            airport_database_menu() 

        elif menu_choice == "4":

            show_history()

            input("\nPress Enter to return to the menu...")

        elif menu_choice == "5":

            show_statistics()

            input("\nPress Enter to return to the menu...")

        elif menu_choice == "6":

            update_flight_status()

            input("\nPress Enter to continue...")

        elif menu_choice == "7":

            delete_flight()

            input("\nPress Enter to continue...")

        elif menu_choice == "8":
            
            print("\nThank you for using AeroFlight Suite.")

            break

        else:

            print("\nInvalid choice.")

            input("Press Enter to continue...")

def aircraft_database_menu():

    while True:

        show_aircraft_database()

        print("\n1. Search Aircraft")
        print("2. Return to Main Menu")

        choice = input("\nChoose an option: ")

        if choice == "1":

            search_aircraft()

            input("\nPress Enter to continue...")

        elif choice == "2":

            break

        else:

            print("\nInvalid choice.")            


def airport_database_menu():
    while True:
        show_airport_database()

        print("\n1. Search Airport")
        print("2. Return to Main Menu")

        choice = input("\nChoose an option: ")

        if choice == "1":
            search_airport()
            input("\nPress Enter to continue...")

        elif choice == "2":
            break

        else:
            print("\nInvalid choice.")
