from core.flight import new_flight
from core.history import show_history
from core.statistics import show_statistics
from utils.display import pause, print_menu
from managers.delete_manager import delete_flight
from managers.status_manager import update_flight_status
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
from config.config import (
    PROJECT_TITLE,
    LINE_SMALL,
    MSG_EXIT,
    MSG_INVALID_OPTION,
    PROMPT_MENU_CHOICE,
    MENU_SEARCH,
    MENU_RETURN_MAIN,
    MENU_NEW_FLIGHT,
    MENU_AIRCRAFT_DATABASE,
    MENU_AIRPORT_DATABASE,
    MENU_FLIGHT_HISTORY,
    MENU_STATISTICS,
    MENU_SEARCH_FLIGHT,
    MENU_ADVANCED_SEARCH,
    MENU_FILTER_FLIGHTS,
    MENU_SORT_FLIGHTS,
    MENU_BACKUP_DATABASE,
    MENU_DELETE_FLIGHT,
    MENU_UPDATE_STATUS,
    MENU_EXIT,
    MENU_ITEM_AIRCRAFT,
    MENU_ITEM_AIRPORT,
)

def display_menu_options():
    options = {
        "1": MENU_NEW_FLIGHT,
        "2": MENU_AIRCRAFT_DATABASE,
        "3": MENU_AIRPORT_DATABASE,
        "4": MENU_FLIGHT_HISTORY,
        "5": MENU_STATISTICS,
        "6": MENU_SEARCH_FLIGHT,
        "7": MENU_ADVANCED_SEARCH,
        "8": MENU_FILTER_FLIGHTS,
        "9": MENU_SORT_FLIGHTS,
        "10": MENU_BACKUP_DATABASE,
        "11": MENU_DELETE_FLIGHT,
        "12": MENU_UPDATE_STATUS,
        "13": MENU_EXIT,
    }
    print_menu(options)


def show_main_menu():
    print("\n" + "=" * LINE_SMALL)
    print(f"{PROJECT_TITLE:^{LINE_SMALL}}")
    print("=" * LINE_SMALL)
    display_menu_options()
    print("=" * LINE_SMALL)


def get_user_choice():
    return input(f"\n{PROMPT_MENU_CHOICE}").strip()


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
        "11": delete_flight,
        "12": update_flight_status,
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
            print(f"\n{MSG_EXIT}")
            break
        if execute_menu_option(choice):
            if choice != "10":
                pause()
        else:
            print(f"\n{MSG_INVALID_OPTION}")
            pause()


def display_database_menu(item_name):
    """
    Display database submenu.
    """
    print(f"\n1. {MENU_SEARCH} {item_name}")
    print(f"2. {MENU_RETURN_MAIN}")


def database_menu(show_function, search_function, item_name):
    while True:
        show_function()
        display_database_menu(item_name)
        choice = input(f"\n{PROMPT_MENU_CHOICE}").strip()
        if choice == "1":
            search_function()
            pause()
        elif choice == "2":
            break
        else:
            print(f"\n{MSG_INVALID_OPTION}")
            pause()


def aircraft_database_menu():
    database_menu(
        show_aircraft_database,
        search_aircraft,
        MENU_ITEM_AIRCRAFT,
    )


def airport_database_menu():
    database_menu(
        show_airport_database,
        search_airport,
        MENU_ITEM_AIRPORT,
    )
