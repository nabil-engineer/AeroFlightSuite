from config.config import (
    LINE_LARGE,
    TITLE_SEARCH_RESULTS,
    TITLE_ADVANCED_SEARCH,
    TITLE_FILTER_RESULTS,
    TITLE_DATABASE_BACKUP,
    TITLE_FLIGHT_FILTER,
    TITLE_SORT_FLIGHTS,
    TITLE_SORT_RESULTS,
    MSG_SEARCH_EMPTY,
    MSG_INVALID_CHOICE,
    PROMPT_FLIGHT_NUMBER,
    PROMPT_AIRCRAFT,
    PROMPT_DEPARTURE,
    PROMPT_ARRIVAL,
    PROMPT_CHOOSE_OPTION,
    PROMPT_VALUE,
    PROMPT_MIN_DISTANCE,
    PROMPT_MIN_WEATHER,
    PROMPT_SEARCH,
    MENU_DEPARTURE,
    MENU_ARRIVAL,
    MENU_AIRCRAFT,
    MENU_DISTANCE,
    MENU_WEATHER_FACTOR,
    MENU_STATUS,
    MENU_BACK,
    MENU_DATE,
    MENU_FUEL_COST,
    MENU_FUEL_CONSUMPTION,
    FILTER_DEPARTURE,
    FILTER_ARRIVAL,
    FILTER_AIRCRAFT,
    FILTER_DISTANCE,
    FILTER_WEATHER_FACTOR,
    FILTER_STATUS,
    SORT_DATE,
    SORT_DISTANCE,
    SORT_COST,
    SORT_FUEL,
    SORT_WEATHER,
)

from managers.flight_repository import (
    search,
    advanced_search,
    filter_by,
    sort_by,
    backup,
)

from utils.validation import (
    get_positive_number,
)

from utils.display import (
    print_menu,
    print_title,
    display_flights_table,
)


# ============================================================
# RESULT DISPLAY
# ============================================================


def show_results(title, flights):
    """
    Display search, filter, or sort results.

    Parameters
    ----------
    title : str
        Title displayed above the results.

    flights : iterable
        Flight records returned by the repository.
    """

    print_title(
        title,
        LINE_LARGE,
    )

    display_flights_table(
        flights,
    )


# ============================================================
# MENU DISPLAY
# ============================================================


def show_menu(title, options):
    """
    Display a formatted menu.

    Parameters
    ----------
    title : str
        Menu title.

    options : dict
        Menu options.
    """

    print_title(
        title,
        LINE_LARGE,
    )

    print_menu(
        options,
    )


# ============================================================
# GLOBAL SEARCH
# ============================================================


def search_flight():
    """
    Search flights by a global keyword.

    The actual search operation is delegated
    to the repository layer.
    """

    keyword = input(
        f"\n{PROMPT_SEARCH}"
    ).strip()

    if not keyword:
        print(
            f"\n{MSG_SEARCH_EMPTY}"
        )
        return

    flights = search(
        keyword,
    )

    show_results(
        TITLE_SEARCH_RESULTS,
        flights,
    )


# ============================================================
# ADVANCED SEARCH
# ============================================================


def advanced_flight_search():
    """
    Perform an advanced flight search.

    Empty values are intentionally passed to
    the repository. The repository is responsible
    for translating empty filters into database
    query parameters.
    """

    filters = {
        "flight_number": input(
            PROMPT_FLIGHT_NUMBER
        ).strip(),

        "aircraft": input(
            PROMPT_AIRCRAFT
        ).strip(),

        "departure": input(
            PROMPT_DEPARTURE
        ).strip(),

        "arrival": input(
            PROMPT_ARRIVAL
        ).strip(),
    }

    flights = advanced_search(
        **filters,
    )

    show_results(
        TITLE_ADVANCED_SEARCH,
        flights,
    )


# ============================================================
# FILTER MENU
# ============================================================


def filter_menu():
    """
    Display the flight filtering menu
    and execute the selected filter.
    """

    options = {
        "1": MENU_DEPARTURE,
        "2": MENU_ARRIVAL,
        "3": MENU_AIRCRAFT,
        "4": MENU_DISTANCE,
        "5": MENU_WEATHER_FACTOR,
        "6": MENU_STATUS,
        "7": MENU_BACK,
    }

    show_menu(
        TITLE_FLIGHT_FILTER,
        options,
    )

    choice = input(f"\n{PROMPT_CHOOSE_OPTION}").strip()

    mapping = {
        "1": FILTER_DEPARTURE,
        "2": FILTER_ARRIVAL,
        "3": FILTER_AIRCRAFT,
        "6": FILTER_STATUS,
    }

    # ======================================================
    # TEXT FILTERS
    # ======================================================

    if choice in mapping:

        value = input(PROMPT_VALUE).strip()

        if not value:
            print("\nFilter value cannot be empty.")
            return

        flights = filter_by(
            mapping[choice],
            value,
        )

    # ======================================================
    # DISTANCE
    # ======================================================

    elif choice == "4":

        minimum_distance = get_positive_number(
            PROMPT_MIN_DISTANCE,
        )

        flights = filter_by(
            FILTER_DISTANCE,
            minimum_distance,
        )

    # ======================================================
    # WEATHER FACTOR
    # ======================================================

    elif choice == "5":

        minimum_weather_factor = get_positive_number(
            PROMPT_MIN_WEATHER,
        )

        flights = filter_by(
            FILTER_WEATHER_FACTOR,
            minimum_weather_factor,
        )

    # ======================================================
    # BACK
    # ======================================================

    elif choice == "7":
        return

    # ======================================================
    # INVALID OPTION
    # ======================================================

    else:

        print(MSG_INVALID_CHOICE)

        return

    # ======================================================
    # RESULTS
    # ======================================================

    show_results(
        TITLE_FILTER_RESULTS,
        flights,
    )


# ============================================================
# SORT MENU
# ============================================================


def sort_menu():
    """
    Display the sorting menu and execute
    the selected sorting operation.
    """

    options = {
        "1": (
            MENU_DATE,
            SORT_DATE,
        ),

        "2": (
            MENU_DISTANCE,
            SORT_DISTANCE,
        ),

        "3": (
            MENU_FUEL_COST,
            SORT_COST,
        ),

        "4": (
            MENU_FUEL_CONSUMPTION,
            SORT_FUEL,
        ),

        "5": (
            MENU_WEATHER_FACTOR,
            SORT_WEATHER,
        ),

        "6": (
            MENU_BACK,
            None,
        ),
    }

    while True:

        show_menu(
            TITLE_SORT_FLIGHTS,
            {
                key: value[0]
                for key, value in options.items()
            },
        )

        choice = input(
            f"\n{PROMPT_CHOOSE_OPTION}"
        ).strip()

        if choice == "6":
            return

        if choice not in options:
            print(
                MSG_INVALID_CHOICE
            )
            continue

        sort_type = options[choice][1]

        flights = sort_by(
            sort_type,
        )

        show_results(
            TITLE_SORT_RESULTS,
            flights,
        )


# ============================================================
# DATABASE BACKUP
# ============================================================


def backup_menu():
    """
    Create a database backup and display
    the resulting backup path.

    The actual backup operation is delegated
    to the repository/database layers.

    Returns
    -------
    None
        This is a UI operation. The backup path
        is displayed to the user and is not returned
        to the menu dispatcher.
    """

    print_title(
        TITLE_DATABASE_BACKUP,
        LINE_LARGE,
    )

    try:

        backup_path = backup()

    except FileNotFoundError as error:

        print(
            "\nBackup failed: "
            "Database file not found."
        )

        print(
            f"Details: {error}"
        )

        return

    except RuntimeError as error:

        print(
            f"\nBackup failed: {error}"
        )

        return

    print(
        "\nDatabase backup created successfully."
    )

    print(
        f"Backup file: {backup_path}"
    )
