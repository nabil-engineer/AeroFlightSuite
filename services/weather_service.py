"""
AeroFlight Suite
Weather Service

Business logic responsible for:
- Creating Weather objects.
- Calculating weather impact.
- Calculating fuel correction factor.
- Determining weather severity.

Weather Severity and Weather Factor are intentionally
treated as two different concepts:

Weather Severity
    Represents the operational risk level of the weather.

Weather Factor
    Represents the effect of physical weather conditions
    on fuel consumption.
"""

from models.weather_model import Weather

from config.config import (
    HEADWIND_FACTOR,
    TAILWIND_FACTOR,
    CROSSWIND_FACTOR,
    HOT_TEMPERATURE,
    COLD_TEMPERATURE,
    HOT_TEMPERATURE_FACTOR,
    COLD_TEMPERATURE_FACTOR,
    LOW_PRESSURE,
    HIGH_PRESSURE,
    LOW_PRESSURE_FACTOR,
    HIGH_PRESSURE_FACTOR,
    HIGH_HUMIDITY,
    HIGH_HUMIDITY_FACTOR,
    LOW_VISIBILITY,
    LOW_VISIBILITY_FACTOR,
    MIN_WEATHER_FACTOR,
    HEADWIND,
    TAILWIND,
    CROSSWIND,
    SEVERITY_LOW,
    SEVERITY_MEDIUM,
    SEVERITY_HIGH,
    WEATHER_SCORE_MAJOR,
    WEATHER_SCORE_MINOR,
    WEATHER_SEVERITY_HIGH_SCORE,
    WEATHER_SEVERITY_MEDIUM_SCORE,
    WEATHER_MAJOR_IMPACT,
    WEATHER_MINOR_IMPACT,
    WEATHER_KEY_WIND,
    WEATHER_KEY_TEMPERATURE,
    WEATHER_KEY_PRESSURE,
    WEATHER_KEY_HUMIDITY,
    WEATHER_KEY_VISIBILITY,
)

# ==========================================================
# Weather Condition Severity
# ==========================================================

WEATHER_CONDITION_SEVERITY_SCORE = {
    "Clear": 0,
    "Cloudy": 1,
    "Rain": 2,
    "Storm": 4,
}


# ==========================================================
# Weather Creation
# ==========================================================


def create_weather(
    temperature,
    wind_speed,
    wind_direction,
    pressure,
    humidity,
    visibility=10,
    condition="Clear",
):
    """
    Create and return a Weather object.

    Weather severity is calculated from both:
    - physical weather conditions
    - selected weather condition

    Parameters
    ----------
    temperature : float
        Temperature in Celsius.

    wind_speed : float
        Wind speed in km/h.

    wind_direction : str
        Headwind, Tailwind, or Crosswind.

    pressure : float
        Atmospheric pressure in hPa.

    humidity : float
        Relative humidity percentage.

    visibility : float
        Visibility in kilometers.

    condition : str
        General weather condition.

    Returns
    -------
    Weather
        Fully initialized Weather object.
    """

    severity = calculate_weather_severity(
        temperature=temperature,
        wind_speed=wind_speed,
        wind_direction=wind_direction,
        pressure=pressure,
        humidity=humidity,
        visibility=visibility,
        condition=condition,
    )

    return Weather(
        temperature=temperature,
        wind_speed=wind_speed,
        wind_direction=wind_direction,
        pressure=pressure,
        humidity=humidity,
        visibility=visibility,
        condition=condition,
        severity=severity,
    )


# ==========================================================
# Weather Severity
# ==========================================================


def calculate_weather_severity(
    temperature,
    wind_speed,
    wind_direction,
    pressure,
    humidity,
    visibility,
    condition="Clear",
):
    """
    Determine the operational weather severity.

    Severity combines:
    1. General weather condition.
    2. Physical weather impacts.

    The condition provides a baseline risk while the
    physical weather parameters can increase that risk.

    Returns
    -------
    str
        Low, Medium, or High.
    """

    impact = calculate_weather_impact(
        temperature=temperature,
        wind_speed=wind_speed,
        wind_direction=wind_direction,
        pressure=pressure,
        humidity=humidity,
        visibility=visibility,
    )

    score = WEATHER_CONDITION_SEVERITY_SCORE.get(
        condition,
        0,
    )

    for value in impact.values():

        if value >= WEATHER_MAJOR_IMPACT:
            score += WEATHER_SCORE_MAJOR

        elif value > WEATHER_MINOR_IMPACT:
            score += WEATHER_SCORE_MINOR

    if score >= WEATHER_SEVERITY_HIGH_SCORE:
        return SEVERITY_HIGH

    if score >= WEATHER_SEVERITY_MEDIUM_SCORE:
        return SEVERITY_MEDIUM

    return SEVERITY_LOW


# ==========================================================
# Weather Impact
# ==========================================================


def calculate_weather_impact(
    temperature,
    wind_speed,
    wind_direction,
    pressure,
    humidity,
    visibility,
):
    """
    Calculate the physical weather impact components.

    This function intentionally does NOT use weather
    condition or severity.

    The returned values are used to calculate the
    fuel correction factor.

    Returns
    -------
    dict
        Individual weather impact values.
    """

    impact = {
        WEATHER_KEY_WIND: 0.0,
        WEATHER_KEY_TEMPERATURE: 0.0,
        WEATHER_KEY_PRESSURE: 0.0,
        WEATHER_KEY_HUMIDITY: 0.0,
        WEATHER_KEY_VISIBILITY: 0.0,
    }

    # ------------------------------------------------------
    # Wind
    # ------------------------------------------------------

    if wind_direction == HEADWIND:

        impact[WEATHER_KEY_WIND] = wind_speed * HEADWIND_FACTOR

    elif wind_direction == TAILWIND:

        impact[WEATHER_KEY_WIND] = -wind_speed * TAILWIND_FACTOR

    elif wind_direction == CROSSWIND:

        impact[WEATHER_KEY_WIND] = wind_speed * CROSSWIND_FACTOR

    # ------------------------------------------------------
    # Temperature
    # ------------------------------------------------------

    if temperature >= HOT_TEMPERATURE:

        impact[WEATHER_KEY_TEMPERATURE] = HOT_TEMPERATURE_FACTOR

    elif temperature <= COLD_TEMPERATURE:

        impact[WEATHER_KEY_TEMPERATURE] = COLD_TEMPERATURE_FACTOR

    # ------------------------------------------------------
    # Pressure
    # ------------------------------------------------------

    if pressure < LOW_PRESSURE:

        impact[WEATHER_KEY_PRESSURE] = LOW_PRESSURE_FACTOR

    elif pressure > HIGH_PRESSURE:

        impact[WEATHER_KEY_PRESSURE] = HIGH_PRESSURE_FACTOR

    # ------------------------------------------------------
    # Humidity
    # ------------------------------------------------------

    if humidity >= HIGH_HUMIDITY:

        impact[WEATHER_KEY_HUMIDITY] = HIGH_HUMIDITY_FACTOR

    # ------------------------------------------------------
    # Visibility
    # ------------------------------------------------------

    if visibility < LOW_VISIBILITY:

        impact[WEATHER_KEY_VISIBILITY] = LOW_VISIBILITY_FACTOR

    return impact


# ==========================================================
# Weather Factor
# ==========================================================


def calculate_weather_factor(weather):
    """
    Calculate the fuel correction factor.

    Weather Factor is based only on physical weather
    impacts and is independent from Weather Severity.

    A value of:

        1.000
            Normal fuel consumption.

        > 1.000
            Increased fuel requirement.

        < 1.000
            Reduced fuel requirement.

    The configured minimum factor is always respected.

    Returns
    -------
    float
        Weather fuel correction factor.
    """

    impact = calculate_weather_impact(
        temperature=weather.temperature,
        wind_speed=weather.wind_speed,
        wind_direction=weather.wind_direction,
        pressure=weather.pressure,
        humidity=weather.humidity,
        visibility=weather.visibility,
    )

    factor = 1.0 + sum(impact.values())

    return max(
        factor,
        MIN_WEATHER_FACTOR,
    )
