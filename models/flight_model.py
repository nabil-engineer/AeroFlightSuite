class Flight:

    def __init__(
        self,
        flight_number,
        flight_date,
        pilot,
        manufacturer,
        model,
        departure_code,
        departure_city,
        arrival_code,
        arrival_city,
        distance,
        speed,
        fuel_price,
        flight_time,
        fuel_needed,
        fuel_cost,
        status,
    ):

        self.flight_number = flight_number
        self.flight_date = flight_date
        self.pilot = pilot
        self.manufacturer = manufacturer
        self.model = model
        self.departure_code = departure_code
        self.departure_city = departure_city
        self.arrival_code = arrival_code
        self.arrival_city = arrival_city
        self.distance = distance
        self.speed = speed
        self.fuel_price = fuel_price
        self.flight_time = flight_time
        self.fuel_needed = fuel_needed
        self.fuel_cost = fuel_cost
        self.status = status

    def aircraft_name(self):
        return f"{self.manufacturer} {self.model}"

    def route(self):
        return (
            f"{self.departure_city} ({self.departure_code})"
            f" -> "
            f"{self.arrival_city} ({self.arrival_code})"
        )

    def to_tuple(self):
        return (
            self.flight_number,
            self.flight_date,
            self.pilot,
            self.manufacturer,
            self.model,
            self.departure_code,
            self.departure_city,
            self.arrival_code,
            self.arrival_city,
            self.distance,
            self.speed,
            self.fuel_price,
            self.flight_time,
            self.fuel_needed,
            self.fuel_cost,
            self.status,
        )


    def __str__(self):
        return f"{self.flight_number} - {self.route()}"
