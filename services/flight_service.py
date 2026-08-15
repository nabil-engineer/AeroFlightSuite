"""
AeroFlight Suite
Flight Service

Version 5.0

Business logic responsible for creating flights and
calculating flight-related metrics.

Weather calculations are delegated to weather_service.
Runway performance calculations are delegated to
runway_service.
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

from services.runway_service import (
    generate_runway_performance_report,
)


class FlightService:
    """
    Business service responsible for flight creation
    and flight-related calculations.
    """

    # ==========================================================
    # FLIGHT METRICS
    # ==========================================================

    def calculate_flight_metrics(
        self,
        aircraft,
        distance,
        fuel_price,
        weather,
    ):
        """
        Calculate flight time, weather factor,
        fuel required, and fuel cost.

       Version 5
       ---------
       Aircraft fuel consumption is read from the aircraft
       data contract without inventing or silently defaulting
       a value.

       Supported fuel-rate fields:

       1. fuel_rate
          Canonical V5 field.

       2. fuel_consumption
          Legacy V4/V5 compatibility field.

       3. fuel_consumption_rate
          Compatibility alias for aircraft data sources.

       4. fuel_per_hour
          Compatibility alias for aircraft data sources.
       """

        # ======================================================
        # AIRCRAFT VALIDATION
        # ======================================================

        if not aircraft or not hasattr(aircraft, "get"):
            raise ValueError("Aircraft data is required.")

        # ======================================================
        # AIRCRAFT SPEED
        # ======================================================

        speed = aircraft.get("speed")

        if speed is None:
            raise ValueError("Aircraft speed is required.")

        try:
            speed = float(speed)
        except (TypeError, ValueError) as error:
            raise ValueError(
                "Aircraft speed must be a valid number."
            ) from error

        if speed <= 0:
            raise ValueError(
                "Aircraft speed must be greater than zero."
            )

        # ======================================================
        # FUEL RATE
        # ======================================================

        # ------------------------------------------------------
        # Canonical V5 field
        # ------------------------------------------------------

        fuel_rate = aircraft.get("fuel_rate")

        # ------------------------------------------------------
        # Legacy V4/V5 compatibility
        # ------------------------------------------------------

        if fuel_rate is None:
            fuel_rate = aircraft.get("fuel_consumption")

        # ------------------------------------------------------
        # Additional compatibility aliases
        # ------------------------------------------------------

        if fuel_rate is None:
            fuel_rate = aircraft.get("fuel_consumption_rate")

        if fuel_rate is None:
            fuel_rate = aircraft.get("fuel_per_hour")

        # ------------------------------------------------------
        # Final validation
        # ------------------------------------------------------

        if fuel_rate is None:
            raise ValueError(
                "Aircraft fuel rate is required. "
                "Expected one of: fuel_rate, "
                "fuel_consumption, fuel_consumption_rate, "
                "or fuel_per_hour."
            )

        try:
            fuel_rate = float(fuel_rate)
        except (TypeError, ValueError) as error:
            raise ValueError(
                "Aircraft fuel rate must be a valid number."
            ) from error

        if fuel_rate <= 0:
            raise ValueError(
                "Aircraft fuel rate must be greater than zero."
            )

        # ======================================================
        # FLIGHT TIME
        # ======================================================

        flight_time = calculate_flight_time(
            distance,
            speed,
        )

        # ======================================================
        # WEATHER FACTOR
        # ======================================================

        if weather is None:

           weather_factor = 1.0

        else:

           weather_factor = calculate_weather_factor(
            weather,
          )

        # ======================================================
        # FUEL NEEDED
        # ======================================================

        fuel_needed = calculate_fuel_needed(
           distance,
           fuel_rate,
           weather_factor,
        )

        # ======================================================
        # FUEL COST
        # ======================================================

        fuel_cost = calculate_fuel_cost(
           fuel_needed,
           fuel_price,
        )

        # ======================================================
        # RESULT
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
    # RUNWAY PERFORMANCE
    # ==========================================================

    def calculate_runway_performance(
        self,
        runway,
        aircraft,
        base_takeoff_distance=None,
        base_landing_distance=None,
        aircraft_weight=None,
        reference_weight=None,
        temperature=None,
    ):
        """
        Calculate a complete Version 5 runway
        performance report.

        Runway performance is optional.

        If runway is None, None is returned.
        """

        # ------------------------------------------------------
        # RUNWAY IS OPTIONAL
        # ------------------------------------------------------

        if runway is None:
            return None

        # ------------------------------------------------------
        # AIRCRAFT VALIDATION
        # ------------------------------------------------------

        if not aircraft or not hasattr(aircraft, "get"):
            raise ValueError("Aircraft data is required for runway performance.")

        # ------------------------------------------------------
        # TAKEOFF DISTANCE
        # ------------------------------------------------------

        if base_takeoff_distance is None:
            base_takeoff_distance = aircraft.get("takeoff_distance")

        if base_takeoff_distance is None:
            raise ValueError(
                "Aircraft takeoff distance is required " "for runway performance."
            )

        # ------------------------------------------------------
        # LANDING DISTANCE
        # ------------------------------------------------------

        if base_landing_distance is None:
            base_landing_distance = aircraft.get("landing_distance")

        if base_landing_distance is None:
            raise ValueError(
                "Aircraft landing distance is required " "for runway performance."
            )

        # ------------------------------------------------------
        # REFERENCE WEIGHT
        # ------------------------------------------------------

        if reference_weight is None:
            reference_weight = aircraft.get("reference_weight")

        # ------------------------------------------------------
        # AIRCRAFT WEIGHT
        # ------------------------------------------------------

        if aircraft_weight is None:
            aircraft_weight = aircraft.get("aircraft_weight")

        # ------------------------------------------------------
        # TEMPERATURE
        # ------------------------------------------------------

        if temperature is None:
            temperature = 15.0

        # ------------------------------------------------------
        # WEIGHT CONSISTENCY
        # ------------------------------------------------------

        # The runway service applies the weight factor only
        # when both actual and reference weights are available.
        #
        # Therefore, if one weight is supplied without the
        # other, fail early instead of silently calculating
        # an incomplete weight adjustment.

        if aircraft_weight is not None and reference_weight is None:
            raise ValueError(
                "Reference weight is required when " "aircraft weight is provided."
            )

        if reference_weight is not None and aircraft_weight is None:
            raise ValueError(
                "Aircraft weight is required when " "reference weight is provided."
            )

        # ------------------------------------------------------
        # PERFORMANCE REPORT
        # ------------------------------------------------------

        return generate_runway_performance_report(
            runway=runway,
            base_takeoff_distance=base_takeoff_distance,
            base_landing_distance=base_landing_distance,
            aircraft_weight=aircraft_weight,
            reference_weight=reference_weight,
            temperature=temperature,
        )

    # ==========================================================
    # FLIGHT CREATION
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
        runway=None,
        base_takeoff_distance=None,
        base_landing_distance=None,
        aircraft_weight=None,
        reference_weight=None,
        temperature=None,
    ):
        """
        Create and return a complete Flight domain object.

        Version 5 additionally supports optional runway
        selection and runway performance analysis.
        """

        # ------------------------------------------------------
        # AIRCRAFT VALIDATION
        # ------------------------------------------------------

        if not aircraft or not hasattr(aircraft, "get"):
            raise ValueError("Aircraft data is required.")

        if not aircraft.get("manufacturer"):
            raise ValueError("Aircraft manufacturer is required.")

        if not aircraft.get("model"):
            raise ValueError("Aircraft model is required.")

        # ------------------------------------------------------
        # FLIGHT METRICS
        # ------------------------------------------------------

        metrics = self.calculate_flight_metrics(
            aircraft=aircraft,
            distance=distance,
            fuel_price=fuel_price,
            weather=weather,
        )

        # ------------------------------------------------------
        # PERFORMANCE TEMPERATURE
        # ------------------------------------------------------

        performance_temperature = temperature

        if performance_temperature is None:

            if weather is not None and hasattr(weather, "temperature"):
                performance_temperature = weather.temperature

            else:
                performance_temperature = 15.0


        # ------------------------------------------------------
        # V5 AIRCRAFT PERFORMANCE WEIGHTS
        # ------------------------------------------------------

        # Explicit arguments have priority.
        # If they are not provided, use the aircraft reference data.

        if reference_weight is None:
           reference_weight = aircraft.get("reference_weight")

        if aircraft_weight is None:
           aircraft_weight = aircraft.get("aircraft_weight")

        # If no actual aircraft weight is supplied,
        # use the reference weight as the baseline operating weight.
        #
        # This keeps the standard aircraft reference dataset
        # compatible with runway performance calculations.
        if aircraft_weight is None and reference_weight is not None:
            aircraft_weight = reference_weight        

        # ------------------------------------------------------
        # RUNWAY PERFORMANCE
        # ------------------------------------------------------

        runway_performance = self.calculate_runway_performance(
            runway=runway,
            aircraft=aircraft,
            base_takeoff_distance=base_takeoff_distance,
            base_landing_distance=base_landing_distance,
            aircraft_weight=aircraft_weight,
            reference_weight=reference_weight,
            temperature=performance_temperature,
        )

        # ------------------------------------------------------
        # FLIGHT OBJECT
        # ------------------------------------------------------

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
            runway=runway,
            runway_performance=runway_performance,
        )


# ==========================================================
# PUBLIC FACTORY
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
    runway=None,
    base_takeoff_distance=None,
    base_landing_distance=None,
    aircraft_weight=None,
    reference_weight=None,
    temperature=None,
):
    """
    Public factory preserving the module-level API.
    """

    return FlightService().create_flight(
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
        runway=runway,
        base_takeoff_distance=base_takeoff_distance,
        base_landing_distance=base_landing_distance,
        aircraft_weight=aircraft_weight,
        reference_weight=reference_weight,
        temperature=temperature,
    )
 