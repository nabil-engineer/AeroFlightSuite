"""
AeroFlight Suite
Runway Performance Service

Version 5.0

Provides runway performance calculations.

Responsibilities
----------------
- Calculate takeoff distance
- Calculate landing distance
- Apply airport/runway elevation effects
- Apply aircraft weight effects
- Apply temperature effects
- Apply runway surface effects
- Compare required distance with available runway length

Architecture
------------
Runway Model
      ↓
Runway Performance Service
      ↓
Core / UI

The service contains business calculations only.

Database access, UI handling, and menu logic do not
belong in this module.
"""

from models.runway_model import Runway

# ============================================================
# CONSTANTS
# ============================================================

DEFAULT_TEMPERATURE = 15.0
STANDARD_PRESSURE = 1013.25

STANDARD_ELEVATION_FACTOR = 0.07
TEMPERATURE_FACTOR = 0.01
WEIGHT_FACTOR = 0.10

# Landing performance adjustment.
# The base landing distance is converted into the
# operational landing requirement before environmental
# and aircraft-performance factors are applied.
LANDING_DISTANCE_FACTOR = 0.60

SURFACE_FACTORS = {
    "asphalt": 1.00,
    "concrete": 1.00,
    "grass": 1.20,
    "gravel": 1.25,
    "wet": 1.15,
}


# ============================================================
# VALIDATION
# ============================================================


def _validate_positive(value, field_name):
    """
    Validate that a numeric value is positive.

    Parameters
    ----------
    value : float
        Value to validate.

    field_name : str
        Name used in the error message.

    Returns
    -------
    float
        Validated numeric value.
    """

    try:
        numeric_value = float(value)
    except (TypeError, ValueError) as error:
        raise ValueError(f"{field_name} must be a numeric value.") from error

    if numeric_value <= 0:
        raise ValueError(f"{field_name} must be greater than zero.")

    return numeric_value


def _validate_runway(runway):
    """
    Validate a runway object.

    Parameters
    ----------
    runway : Runway
        Runway instance.

    Raises
    ------
    TypeError
        If the supplied object is not a Runway.

    ValueError
        If runway length is invalid.
    """

    if not isinstance(runway, Runway):
        raise TypeError("runway must be an instance of Runway.")

    _validate_positive(
        runway.length,
        "Runway length",
    )


# ============================================================
# ENVIRONMENT FACTORS
# ============================================================


def calculate_elevation_factor(elevation):
    """
    Calculate the runway elevation performance factor.

    Higher elevation generally reduces aircraft performance.

    This is a simplified Version 5 engineering model and
    is intended for portfolio/software simulation purposes.

    Parameters
    ----------
    elevation : float
        Airport/runway elevation in meters.

    Returns
    -------
    float
        Elevation performance factor.
    """

    try:
        elevation = float(elevation or 0)
    except (TypeError, ValueError) as error:
        raise ValueError("Elevation must be numeric.") from error

    if elevation < 0:
        elevation = 0

    return 1.0 + (elevation / 1000.0) * STANDARD_ELEVATION_FACTOR


def calculate_temperature_factor(
    temperature=DEFAULT_TEMPERATURE,
):
    """
    Calculate the temperature performance factor.

    Standard reference temperature is 15°C.

    Higher temperatures increase required runway distance.

    Parameters
    ----------
    temperature : float
        Ambient temperature in Celsius.

    Returns
    -------
    float
        Temperature performance factor.
    """

    try:
        temperature = float(temperature)
    except (TypeError, ValueError) as error:
        raise ValueError("Temperature must be numeric.") from error

    temperature_difference = temperature - DEFAULT_TEMPERATURE

    factor = 1.0 + (temperature_difference * TEMPERATURE_FACTOR)

    return max(
        factor,
        0.50,
    )


def calculate_weight_factor(
    aircraft_weight,
    reference_weight,
):
    """
    Calculate the performance factor caused by aircraft weight.

    Parameters
    ----------
    aircraft_weight : float
        Actual aircraft weight in kilograms.

    reference_weight : float
        Reference aircraft weight in kilograms.

    Returns
    -------
    float
        Weight performance factor.
    """

    aircraft_weight = _validate_positive(
        aircraft_weight,
        "Aircraft weight",
    )

    reference_weight = _validate_positive(
        reference_weight,
        "Reference weight",
    )

    ratio = aircraft_weight / reference_weight

    return 1.0 + ((ratio - 1.0) * WEIGHT_FACTOR)


def calculate_surface_factor(surface):
    """
    Return the runway surface performance factor.

    Parameters
    ----------
    surface : str
        Runway surface.

    Returns
    -------
    float
        Surface factor.
    """

    normalized_surface = (
        str(surface).strip().lower() if surface is not None else "asphalt"
    )

    return SURFACE_FACTORS.get(
        normalized_surface,
        1.0,
    )


# ============================================================
# TAKEOFF PERFORMANCE
# ============================================================


def calculate_required_takeoff_distance(
    runway,
    base_takeoff_distance,
    aircraft_weight=None,
    reference_weight=None,
    temperature=DEFAULT_TEMPERATURE,
):
    """
    Calculate the estimated required takeoff distance.

    Parameters
    ----------
    runway : Runway
        Runway used for the operation.

    base_takeoff_distance : float
        Aircraft reference takeoff distance in meters.

    aircraft_weight : float, optional
        Actual aircraft weight in kilograms.

    reference_weight : float, optional
        Reference weight in kilograms.

    temperature : float, optional
        Ambient temperature in Celsius.

    Returns
    -------
    float
        Estimated required takeoff distance in meters.
    """

    _validate_runway(runway)

    base_distance = _validate_positive(
        base_takeoff_distance,
        "Base takeoff distance",
    )

    elevation_factor = calculate_elevation_factor(runway.elevation)

    temperature_factor = calculate_temperature_factor(temperature)

    surface_factor = calculate_surface_factor(runway.surface)

    weight_factor = 1.0

    if aircraft_weight is not None and reference_weight is not None:
        weight_factor = calculate_weight_factor(
            aircraft_weight,
            reference_weight,
        )

    required_distance = (
        base_distance
        * elevation_factor
        * temperature_factor
        * surface_factor
        * weight_factor
    )

    return round(
        required_distance,
        2,
    )


# ============================================================
# LANDING PERFORMANCE
# ============================================================


def calculate_required_landing_distance(
    runway,
    base_landing_distance,
    aircraft_weight=None,
    reference_weight=None,
    temperature=DEFAULT_TEMPERATURE,
):
    """
    Calculate the estimated required landing distance.

    The landing calculation uses the dedicated
    LANDING_DISTANCE_FACTOR before applying environmental
    and aircraft-performance factors.

    Parameters
    ----------
    runway : Runway
        Runway used for landing.

    base_landing_distance : float
        Aircraft reference landing distance in meters.

    aircraft_weight : float, optional
        Actual aircraft weight in kilograms.

    reference_weight : float, optional
        Reference weight in kilograms.

    temperature : float, optional
        Ambient temperature in Celsius.

    Returns
    -------
    float
        Estimated required landing distance in meters.
    """

    _validate_runway(runway)

    base_distance = _validate_positive(
        base_landing_distance,
        "Base landing distance",
    )

    # --------------------------------------------------------
    # Landing-specific baseline
    # --------------------------------------------------------
    #
    # Keep the landing calculation independent from takeoff.
    # The dedicated landing factor is applied first, then the
    # environmental and weight factors are applied.
    #
    landing_base_distance = base_distance * LANDING_DISTANCE_FACTOR

    elevation_factor = calculate_elevation_factor(runway.elevation)

    temperature_factor = calculate_temperature_factor(temperature)

    surface_factor = calculate_surface_factor(runway.surface)

    weight_factor = 1.0

    if aircraft_weight is not None and reference_weight is not None:
        weight_factor = calculate_weight_factor(
            aircraft_weight,
            reference_weight,
        )

    required_distance = (
        landing_base_distance
        * elevation_factor
        * temperature_factor
        * surface_factor
        * weight_factor
    )

    return round(
        required_distance,
        2,
    )


# ============================================================
# RUNWAY AVAILABILITY
# ============================================================


def calculate_takeoff_margin(
    runway,
    required_takeoff_distance,
):
    """
    Calculate remaining runway available after takeoff
    performance requirements.

    Parameters
    ----------
    runway : Runway
        Selected runway.

    required_takeoff_distance : float
        Required takeoff distance in meters.

    Returns
    -------
    float
        Remaining runway margin in meters.
    """

    _validate_runway(runway)

    required_distance = _validate_positive(
        required_takeoff_distance,
        "Required takeoff distance",
    )

    return round(
        float(runway.length) - required_distance,
        2,
    )


def calculate_landing_margin(
    runway,
    required_landing_distance,
):
    """
    Calculate remaining runway available after landing
    performance requirements.

    Parameters
    ----------
    runway : Runway
        Selected runway.

    required_landing_distance : float
        Required landing distance in meters.

    Returns
    -------
    float
        Remaining runway margin in meters.
    """

    _validate_runway(runway)

    required_distance = _validate_positive(
        required_landing_distance,
        "Required landing distance",
    )

    return round(
        float(runway.length) - required_distance,
        2,
    )


# ============================================================
# PERFORMANCE STATUS
# ============================================================


def evaluate_runway_performance(
    runway,
    required_distance,
):
    """
    Evaluate whether the available runway is sufficient.

    Parameters
    ----------
    runway : Runway
        Selected runway.

    required_distance : float
        Required runway distance in meters.

    Returns
    -------
    dict
        Performance evaluation.
    """

    _validate_runway(runway)

    required_distance = _validate_positive(
        required_distance,
        "Required distance",
    )

    available_distance = float(runway.length)

    margin = round(
        available_distance - required_distance,
        2,
    )

    return {
        "airport_code": runway.airport_code,
        "runway_id": runway.runway_id,
        "available_distance": available_distance,
        "required_distance": required_distance,
        "margin": margin,
        "sufficient": margin >= 0,
        "status": ("SUFFICIENT" if margin >= 0 else "INSUFFICIENT"),
    }


# ============================================================
# COMPLETE PERFORMANCE REPORT
# ============================================================


def generate_runway_performance_report(
    runway,
    base_takeoff_distance,
    base_landing_distance,
    aircraft_weight=None,
    reference_weight=None,
    temperature=DEFAULT_TEMPERATURE,
):
    """
    Generate a complete runway performance report.

    The report combines takeoff and landing calculations
    while keeping the service independent from the UI.

    Version 5
    ---------
    The report preserves the aircraft performance inputs
    used during calculation so the repository/database layer
    can persist the exact performance context.

    Returns
    -------
    dict
        Complete runway performance report.
    """

    # ======================================================
    # TAKEOFF PERFORMANCE
    # ======================================================

    required_takeoff_distance = calculate_required_takeoff_distance(
        runway=runway,
        base_takeoff_distance=base_takeoff_distance,
        aircraft_weight=aircraft_weight,
        reference_weight=reference_weight,
        temperature=temperature,
    )

    # ======================================================
    # LANDING PERFORMANCE
    # ======================================================

    required_landing_distance = calculate_required_landing_distance(
        runway=runway,
        base_landing_distance=base_landing_distance,
        aircraft_weight=aircraft_weight,
        reference_weight=reference_weight,
        temperature=temperature,
    )

    # ======================================================
    # TAKEOFF EVALUATION
    # ======================================================

    takeoff_evaluation = evaluate_runway_performance(
        runway,
        required_takeoff_distance,
    )

    # ======================================================
    # LANDING EVALUATION
    # ======================================================

    landing_evaluation = evaluate_runway_performance(
        runway,
        required_landing_distance,
    )

    # ======================================================
    # COMPLETE PERFORMANCE REPORT
    # ======================================================

    return {
        "airport_code": runway.airport_code,
        "runway_id": runway.runway_id,
        "runway_length": float(runway.length),
        "runway_surface": runway.surface,
        "runway_elevation": float(runway.elevation or 0),
        # --------------------------------------------------
        # PERFORMANCE INPUTS
        # --------------------------------------------------
        "temperature": float(temperature),
        "aircraft_weight": (
            float(aircraft_weight) if aircraft_weight is not None else None
        ),
        "reference_weight": (
            float(reference_weight) if reference_weight is not None else None
        ),
        # --------------------------------------------------
        # REQUIRED DISTANCES
        # --------------------------------------------------
        "required_takeoff_distance": required_takeoff_distance,
        "required_landing_distance": required_landing_distance,
        # --------------------------------------------------
        # RUNWAY MARGINS
        # --------------------------------------------------
        "takeoff_margin": takeoff_evaluation["margin"],
        "landing_margin": landing_evaluation["margin"],
        # --------------------------------------------------
        # PERFORMANCE STATUS
        # --------------------------------------------------
        "takeoff_status": takeoff_evaluation["status"],
        "landing_status": landing_evaluation["status"],
        "takeoff_sufficient": takeoff_evaluation["sufficient"],
        "landing_sufficient": landing_evaluation["sufficient"],
    }
