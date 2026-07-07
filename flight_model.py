class Flight:

    def __init__(
        self,
        pilot,
        manufacturer,
        model,
        departure_city,
        arrival_city,
        distance,
        speed,
        fuel_price,
        flight_time,
        fuel_needed,
        fuel_cost
    ):

        self.pilot = pilot
        self.manufacturer = manufacturer
        self.model = model
        self.departure_city = departure_city
        self.arrival_city = arrival_city
        self.distance = distance
        self.speed = speed
        self.fuel_price = fuel_price
        self.flight_time = flight_time
        self.fuel_needed = fuel_needed
        self.fuel_cost = fuel_cost

    def aircraft_name(self):
        return f"{self.manufacturer} {self.model}"

    def route(self):
        return f"{self.departure_city} -> {self.arrival_city}"