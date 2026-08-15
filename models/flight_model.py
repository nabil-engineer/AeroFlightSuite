"""
AeroFlight Suite
Flight Model

Domain model representing a complete flight record.

The model stores flight information, aircraft information,
route information, fuel calculations, weather intelligence,
and the optional Version 5 runway selection/performance report.

Business calculations are handled by services.
Database persistence is handled by repositories.
"""

from config.config import DEFAULT_STATUS


class Flight:
    """
    Represent a complete AeroFlight Suite flight.
    """

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
        weather=None,
        weather_factor=1.0,
        status=DEFAULT_STATUS,
        runway=None,
        runway_performance=None,
    ):
        # ======================================================
        # FLIGHT INFORMATION
        # ======================================================

        self.flight_number = flight_number
        self.flight_date = flight_date
        self.pilot = pilot
        self.status = status
        self.runway_performance = runway_performance

        # ======================================================
        # AIRCRAFT INFORMATION
        # ======================================================

        self.manufacturer = manufacturer
        self.model = model

        # ======================================================
        # ROUTE INFORMATION
        # ======================================================

        self.departure_code = departure_code
        self.departure_city = departure_city

        self.arrival_code = arrival_code
        self.arrival_city = arrival_city

        # ======================================================
        # FLIGHT CALCULATIONS
        # ======================================================

        self.distance = distance
        self.speed = speed
        self.fuel_price = fuel_price
        self.flight_time = flight_time
        self.fuel_needed = fuel_needed
        self.fuel_cost = fuel_cost

        # ======================================================
        # WEATHER INTELLIGENCE
        # ======================================================

        self.weather = weather
        self.weather_factor = weather_factor

        # ======================================================
        # VERSION 5 - RUNWAY
        # ======================================================

        self.runway = runway
        self.runway_performance = runway_performance

    # ==========================================================
    # AIRCRAFT
    # ==========================================================

    @property
    def aircraft(self):
        """
        Return the complete aircraft display name.
        """

        manufacturer = (
            str(self.manufacturer).strip() if self.manufacturer is not None else ""
        )

        model = str(self.model).strip() if self.model is not None else ""

        return " ".join(
            part
            for part in (
                manufacturer,
                model,
            )
            if part
        )

    # ==========================================================
    # DEPARTURE
    # ==========================================================

    @property
    def departure(self):
        """
        Return the formatted departure airport.
        """

        code = (
            str(self.departure_code).strip() if self.departure_code is not None else ""
        )

        city = (
            str(self.departure_city).strip() if self.departure_city is not None else ""
        )

        if code and city:

            return f"{code} - {city}"

        return code or city

    # ==========================================================
    # ARRIVAL
    # ==========================================================

    @property
    def arrival(self):
        """
        Return the formatted arrival airport.
        """

        code = str(self.arrival_code).strip() if self.arrival_code is not None else ""

        city = str(self.arrival_city).strip() if self.arrival_city is not None else ""

        if code and city:

            return f"{code} - {city}"

        return code or city

    # ==========================================================
    # ROUTE
    # ==========================================================

    @property
    def route(self):
        """
        Return the complete formatted flight route.
        """

        return f"{self.departure} -> " f"{self.arrival}"

    # ==========================================================
    # FUEL COMPATIBILITY
    # ==========================================================

    @property
    def fuel_consumption(self):
        """
        Return the legacy fuel field.

        ``fuel_needed`` remains the canonical
        flight-level fuel field.
        """

        return self.fuel_needed

    # ==========================================================
    # RUNWAY
    # ==========================================================

    @property
    def runway_id(self):
        """
        Return the selected runway identifier.
        """

        if self.runway is None:
            return None

        return getattr(
            self.runway,
            "runway_id",
            None,
        )

    @property
    def runway_airport_code(self):
        """
        Return the airport code associated
        with the selected runway.
        """

        if self.runway is None:
            return None

        return getattr(
            self.runway,
            "airport_code",
            None,
        )

    # ==========================================================
    # WEATHER
    # ==========================================================

    def weather_data(self):
        """
        Return complete normalized weather information.
        """

        if self.weather is None:

            return {
                "wind_speed": 0,
                "wind_direction": "",
                "temperature": 0,
                "pressure": 0,
                "humidity": 0,
                "visibility": 0,
                "condition": "",
                "severity": "",
                "weather_factor": (self.weather_factor),
            }

        data = self.weather.to_dict()

        return {
            "wind_speed": data.get(
                "wind_speed",
                0,
            ),
            "wind_direction": data.get(
                "wind_direction",
                "",
            ),
            "temperature": data.get(
                "temperature",
                0,
            ),
            "pressure": data.get(
                "pressure",
                0,
            ),
            "humidity": data.get(
                "humidity",
                0,
            ),
            "visibility": data.get(
                "visibility",
                0,
            ),
            "condition": data.get(
                "condition",
                data.get(
                    "weather_condition",
                    "",
                ),
            ),
            "severity": data.get(
                "severity",
                data.get(
                    "weather_severity",
                    "",
                ),
            ),
            "weather_factor": (self.weather_factor),
        }

    # ==========================================================
    # SERIALIZATION
    # ==========================================================

    def to_tuple(self):
        """
        Return the legacy flight tuple.

        Version 5 runway data is deliberately excluded
        because runway performance has its own persistence
        contract.
        """

        weather = self.weather_data()

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
            weather.get(
                "wind_speed",
                0,
            ),
            weather.get(
                "wind_direction",
                "",
            ),
            weather.get(
                "temperature",
                0,
            ),
            weather.get(
                "pressure",
                0,
            ),
            weather.get(
                "humidity",
                0,
            ),
            weather.get(
                "visibility",
                0,
            ),
            weather.get(
                "condition",
                "",
            ),
            weather.get(
                "severity",
                "",
            ),
            self.weather_factor,
            self.fuel_price,
            self.flight_time,
            self.fuel_needed,
            self.fuel_cost,
            self.status,
        )

    # ==========================================================
    # REPRESENTATION
    # ==========================================================

    def __str__(self):
        """
        Return a concise human-readable representation.
        """

        runway = self.runway_id or "N/A"

        try:

            weather_factor = f"{float(self.weather_factor):.3f}"

        except (
            TypeError,
            ValueError,
        ):

            weather_factor = str(self.weather_factor)

        return (
            f"{self.flight_number} - "
            f"{self.route} | "
            f"Runway: {runway} | "
            f"Weather Factor: "
            f"{weather_factor}"
        )

    def __repr__(self):
        """
        Return a developer-friendly representation.
        """

        return (
            "Flight("
            f"flight_number={self.flight_number!r}, "
            f"flight_date={self.flight_date!r}, "
            f"pilot={self.pilot!r}, "
            f"aircraft={self.aircraft!r}, "
            f"route={self.route!r}, "
            f"distance={self.distance!r}, "
            f"fuel_needed={self.fuel_needed!r}, "
            f"fuel_cost={self.fuel_cost!r}, "
            f"status={self.status!r}, "
            f"runway_id={self.runway_id!r}"
            ")"
        )
