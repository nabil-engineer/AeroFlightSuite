"""
AeroFlight Suite
Runway Model

Domain model representing an airport runway.

A runway is an independent domain entity and is associated
with an airport through its ICAO/IATA airport code.

The model is intentionally designed to support multiple
runways per airport.

Example
-------
Airport RBA
    ├── Runway 04/22
    └── Runway 04L/22R

The runway model contains infrastructure information only.

Performance calculations belong to the runway service layer.
Database persistence belongs to the repository/database layer.
"""


class Runway:
    """
    Represent a single airport runway.

    Parameters
    ----------
    airport_code : str
        Airport code associated with the runway.

    runway_id : str
        Runway identifier, for example ``04/22``.

    length : float
        Runway length in meters.

    width : float
        Runway width in meters.

    surface : str
        Runway surface type.

    elevation : float
        Airport/runway elevation in meters.

    heading : float
        Primary runway magnetic/true heading in degrees.

    """

    def __init__(
        self,
        airport_code,
        runway_id,
        length,
        width=None,
        surface="Asphalt",
        elevation=0.0,
        heading=None,
    ):
        self.airport_code = (
            str(airport_code).strip().upper() if airport_code is not None else ""
        )

        self.runway_id = str(runway_id).strip().upper() if runway_id is not None else ""

        self.length = length
        self.width = width
        self.surface = str(surface).strip() if surface is not None else ""

        self.elevation = elevation
        self.heading = heading

    # ======================================================
    # DISPLAY PROPERTIES
    # ======================================================

    @property
    def display_name(self):
        """
        Return a human-readable runway name.

        Example
        -------
        RBA 04/22
        """

        if self.airport_code and self.runway_id:
            return f"{self.airport_code} " f"{self.runway_id}"

        return self.runway_id or self.airport_code

    # ======================================================
    # SERIALIZATION
    # ======================================================

    def to_dict(self):
        """
        Return the runway as a dictionary.

        Returns
        -------
        dict
            Normalized runway representation.
        """

        return {
            "airport_code": self.airport_code,
            "runway_id": self.runway_id,
            "length": self.length,
            "width": self.width,
            "surface": self.surface,
            "elevation": self.elevation,
            "heading": self.heading,
        }

    # ======================================================
    # REPRESENTATION
    # ======================================================

    def __str__(self):
        """
        Return a concise human-readable representation.
        """

        return f"{self.display_name} | " f"{self.length} m | " f"{self.surface}"

    def __repr__(self):
        """
        Return a developer-friendly representation.
        """

        return (
            "Runway("
            f"airport_code={self.airport_code!r}, "
            f"runway_id={self.runway_id!r}, "
            f"length={self.length!r}, "
            f"width={self.width!r}, "
            f"surface={self.surface!r}, "
            f"elevation={self.elevation!r}, "
            f"heading={self.heading!r}"
            ")"
        )
