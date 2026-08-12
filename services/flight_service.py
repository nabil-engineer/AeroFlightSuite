"""
AeroFlight Suite
Flight Service

Business logic responsible for creating flights
and calculating flight-related metrics.

Weather calculations are delegated to weather_service.
"""

from models.flight_model import Flight

from utils.calculator import (
    calculate_flight_time,
    calculate_fuel_needed,
    calculate_fuel_cost,
)

from services.weather_service import (
    calculate_weather_factor,
)


class FlightService:
    """
    Business service responsible for flight creation
    and flight calculations.
    """

    # ==========================================================
    # Flight Metrics
    # ==========================================================

    def calculate_flight_metrics(
        self,
        aircraft,
        distance,
        fuel_price,
        weather,
    ):
        """
        Calculate all flight metrics.

        Fuel contract
        -------------
        ``fuel_rate`` is the preferred aircraft-level
        fuel consumption field.

        ``fuel_consumption`` is retained as a legacy
        fallback so existing aircraft data continues
        to work without modification.

        The resulting ``fuel_needed`` value is the
        canonical flight-level fuel quantity.

        Returns
        -------
        dict
            Calculated flight metrics.
        """

        if not aircraft:
            raise ValueError("Aircraft data is required.")

        # ======================================================
        # Aircraft Speed
        # ======================================================

        speed = aircraft.get("speed")

        if speed is None:
            raise ValueError("Aircraft speed is required.")

        # ======================================================
        # Aircraft Fuel Rate
        # ======================================================
        #
        # Preferred:
        #     fuel_rate
        #
        # Legacy fallback:
        #     fuel_consumption
        #
        # We intentionally keep the fallback to preserve
        # compatibility with the existing aircraft catalog.
        # ======================================================

        fuel_rate = aircraft.get("fuel_rate")

        if fuel_rate is None:
            fuel_rate = aircraft.get("fuel_consumption")

        if fuel_rate is None:
            raise ValueError("Aircraft fuel rate is required.")

        # ======================================================
        # Flight Time
        # ======================================================

        flight_time = calculate_flight_time(
            distance,
            speed,
        )

        # ======================================================
        # Weather Factor
        # ======================================================

        weather_factor = calculate_weather_factor(
            weather,
        )

        # ======================================================
        # Fuel Needed
        # ======================================================

        fuel_needed = calculate_fuel_needed(
            distance,
            fuel_rate,
            weather_factor,
        )

        # ======================================================
        # Fuel Cost
        # ======================================================

        fuel_cost = calculate_fuel_cost(
            fuel_needed,
            fuel_price,
        )

        # ======================================================
        # Result
        # ======================================================

        return {
            "speed": speed,
            "fuel_rate": fuel_rate,
            "flight_time": flight_time,
            "weather_factor": weather_factor,
            "fuel_needed": fuel_needed,
            "fuel_cost": fuel_cost,
        }

    # ==========================================================
    # Flight Creation
    # ==========================================================

    def create_flight(
        self,
        flight_number,
        flight_date,
        pilot,
        aircraft,
        departure_code,
        departure_city,
        arrival_code,
        arrival_city,
        distance,
        fuel_price,
        weather,
    ):
        """
        Create and return a complete Flight object.
        """

        metrics = self.calculate_flight_metrics(
            aircraft=aircraft,
            distance=distance,
            fuel_price=fuel_price,
            weather=weather,
        )

        return Flight(
            flight_number=flight_number,
            flight_date=flight_date,
            pilot=pilot,
            manufacturer=aircraft["manufacturer"],
            model=aircraft["model"],
            departure_code=departure_code,
            departure_city=departure_city,
            arrival_code=arrival_code,
            arrival_city=arrival_city,
            distance=distance,
            speed=metrics["speed"],
            fuel_price=fuel_price,
            flight_time=metrics["flight_time"],
            fuel_needed=metrics["fuel_needed"],
            fuel_cost=metrics["fuel_cost"],
            weather=weather,
            weather_factor=metrics["weather_factor"],
        )


# ==========================================================
# Public Factory
# ==========================================================


def create_flight(
    flight_number,
    flight_date,
    pilot,
    aircraft,
    departure_code,
    departure_city,
    arrival_code,
    arrival_city,
    distance,
    fuel_price,
    weather,
):
    """
    Public factory for creating a Flight.

    This function keeps backward compatibility with
    callers that use the module-level API.
    """

    service = FlightService()

    return service.create_flight(
        flight_number=flight_number,
        flight_date=flight_date,
        pilot=pilot,
        aircraft=aircraft,
        departure_code=departure_code,
        departure_city=departure_city,
        arrival_code=arrival_code,
        arrival_city=arrival_city,
        distance=distance,
        fuel_price=fuel_price,
        weather=weather,
    )
