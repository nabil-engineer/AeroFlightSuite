from flight import new_flight
from history import show_history
from statistics import show_statistics
from database import show_aircraft_database, search_aircraft

def show_main_menu():

    print("\n" + "=" * 60)
    print("           AEROFLIGHT SUITE")
    print("=" * 60)

    print("1. New Flight")
    print("2. Aircraft Database")
    print("3. Flight History")
    print("4. Statistics")
    print("5. Exit")

    print("=" * 60)

def run_menu():

    while True:

        show_main_menu()

        menu_choice = input("Choose an option: ")

        if menu_choice == "1":

            new_flight()

        elif menu_choice == "2":

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

               

        elif menu_choice == "3":

            show_history()

            input("\nPress Enter to return to the menu...")

        elif menu_choice == "4":

            show_statistics()

            input("\nPress Enter to return to the menu...")

        elif menu_choice == "5":

            print("\nThank you for using AeroFlight Suite.")

            break

        else:

            print("\nInvalid choice.")

            input("Press Enter to continue...")