def validate_pilot_name(name):
    return name.strip() != ""

def validate_city_name(city):

    return city.strip() != ""

def validate_positive_number(value):

    return value > 0

def get_positive_number(message):

    while True:

        try:

            value = float(input(message))

            if validate_positive_number(value):

                return value

            print("Value must be greater than zero.")

        except ValueError:

            print("Please enter a valid number.")

def get_city_name(message):

    while True:

        city = input(message).strip()

        if validate_city_name(city):

            return city

        print("City name cannot be empty.")            

def get_aircraft_choice(aircrafts):

    while True:

        try:

            choice = int(input("\nChoose an aircraft (1-50): "))

            if choice in aircrafts:

                return choice

            print("Please choose a number between 1 and 50.")

        except ValueError:

            print("Please enter a valid integer.")        