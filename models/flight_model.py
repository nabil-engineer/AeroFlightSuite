"""
AeroFlight Suite
Flight Model

Domain model representing a complete flight record.

The model keeps flight data, aircraft information,
route information, fuel calculations, and weather
intelligence in one consistent API.

Business calculations are handled by services.
Database persistence is handled by repositories.
"""

from config.config import DEFAULT_STATUS


class Flight:
    """
    Represent a complete AeroFlight flight.

    The Flight model is responsible for storing domain data
    and exposing convenient domain-level properties.

    Business calculations are handled by services.

    Database persistence is handled by repositories.
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
    ):
        # ==================================================
        # Flight Information
        # ==================================================

        self.flight_number = flight_number
        self.flight_date = flight_date
        self.pilot = pilot
        self.status = status

        # ==================================================
        # Aircraft Information
        # ==================================================

        self.manufacturer = manufacturer
        self.model = model
        self.speed = speed
        self.fuel_price = fuel_price

        # ==================================================
        # Route Information
        # ==================================================

        self.departure_code = departure_code
        self.departure_city = departure_city

        self.arrival_code = arrival_code
        self.arrival_city = arrival_city

        # ==================================================
        # Flight Calculations
        # ==================================================

        self.distance = distance
        self.flight_time = flight_time
        self.fuel_needed = fuel_needed
        self.fuel_cost = fuel_cost

        # ==================================================
        # Weather Intelligence
        # ==================================================

        self.weather = weather
        self.weather_factor = weather_factor

    # ======================================================
    # Derived Properties
    # ======================================================

    @property
    def aircraft(self):
        """
        Return the complete aircraft name.

        Examples
        --------
        Airbus A320
        Boeing 777-300ER
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

    @property
    def route(self):
        """
        Return the complete formatted route.
        """

        return f"{self.departure} -> {self.arrival}"

    # ======================================================
    # Compatibility Properties
    # ======================================================

    @property
    def fuel_consumption(self):
        """
        Return fuel consumption using the legacy
        compatibility name.

        AeroFlight Suite uses ``fuel_needed`` as the
        canonical domain field.

        ``fuel_consumption`` is kept as a compatibility
        alias for older database/statistics code.
        """

        return self.fuel_needed

    # ======================================================
    # Weather API
    # ======================================================

    def weather_data(self):
        """
        Return weather information as a dictionary.

        This method provides a stable API for consumers
        that should not depend directly on the Weather object.

        Returns
        -------
        dict
            Complete normalized weather information.
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
        }

    # ======================================================
    # Dictionary Serialization
    # ======================================================

    def to_dict(self):
        """
        Return the complete flight as a dictionary.

        The dictionary provides a stable domain representation
        for reports, exports, APIs, UI components, and other
        consumers.

        Database-specific persistence remains the
        responsibility of repositories/database functions.
        """

        weather = self.weather_data()

        return {
            # ------------------------------------------------
            # Flight
            # ------------------------------------------------
            "flight_number": self.flight_number,
            "flight_date": self.flight_date,
            "pilot": self.pilot,
            "status": self.status,
            # ------------------------------------------------
            # Aircraft
            # ------------------------------------------------
            "manufacturer": self.manufacturer,
            "model": self.model,
            "aircraft": self.aircraft,
            # ------------------------------------------------
            # Route
            # ------------------------------------------------
            "departure_code": self.departure_code,
            "departure_city": self.departure_city,
            "departure": self.departure,
            "arrival_code": self.arrival_code,
            "arrival_city": self.arrival_city,
            "arrival": self.arrival,
            "route": self.route,
            # ------------------------------------------------
            # Flight calculations
            # ------------------------------------------------
            "distance": self.distance,
            "speed": self.speed,
            "fuel_price": self.fuel_price,
            "flight_time": self.flight_time,
            "fuel_needed": self.fuel_needed,
            # Legacy compatibility name.
            "fuel_consumption": self.fuel_consumption,
            "fuel_cost": self.fuel_cost,
            # ------------------------------------------------
            # Weather
            # ------------------------------------------------
            "wind_speed": weather["wind_speed"],
            "wind_direction": weather["wind_direction"],
            "temperature": weather["temperature"],
            "pressure": weather["pressure"],
            "humidity": weather["humidity"],
            "visibility": weather["visibility"],
            # Current domain names.
            "condition": weather["condition"],
            "severity": weather["severity"],
            # Database-compatible names.
            "weather_condition": weather["condition"],
            "weather_severity": weather["severity"],
            "weather_factor": self.weather_factor,
        }

    # ======================================================
    # String Representation
    # ======================================================

    def __str__(self):
        """
        Return a concise human-readable representation.
        """

        return (
            f"{self.flight_number} | "
            f"{self.aircraft} | "
            f"{self.route} | "
            f"Weather Factor: "
            f"{self.weather_factor:.3f}"
        )
