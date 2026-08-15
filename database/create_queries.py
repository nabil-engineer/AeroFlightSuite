"""
AeroFlight Suite
Database Create Queries

Responsible for:

- Database creation
- Schema versioning
- Schema migrations
- Legacy data migration
- Route normalization
- Index creation
- Flight insertion
"""

import sqlite3
from contextlib import nullcontext

from .common import get_connection
from data.runway_data import runways as RUNWAY_REFERENCE_DATA

# ==========================================================
# DATABASE SCHEMA VERSION
# ==========================================================

CURRENT_SCHEMA_VERSION = 5


# ==========================================================
# DATABASE CREATION / MIGRATION
# ==========================================================


def create_database():
    """
    Create or upgrade the AeroFlight Suite database.

    The official database schema version for AeroFlight
    Suite V4 is version 4.

    Database evolution is handled through explicit,
    versioned migrations.

    Schema repair is intentionally performed only after
    the versioned migrations. This keeps the migration
    history authoritative while still protecting the
    application from databases whose physical schema is
    incomplete or whose user_version is incorrect.

    Workflow
    --------
    1. Open the database.
    2. Read SQLite user_version.
    3. Create the base table when necessary.
    4. Validate the recorded version.
    5. Run required migrations sequentially.
    6. Verify and repair the physical schema.
    7. Normalize legacy data.
    8. Create indexes.
    9. Store the official schema version.
    10. Commit the transaction.
    """

    with get_connection() as connection:

        cursor = connection.cursor()

        # ==================================================
        # READ DATABASE VERSION
        # ==================================================

        current_version = cursor.execute("PRAGMA user_version").fetchone()[0]

        # ==================================================
        # CREATE BASE TABLE
        # ==================================================
        #
        # This definition is used only when the database
        # does not contain the flights table.
        #
        # Existing databases are upgraded through the
        # migration system below.
        # ==================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS flights (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                -- Flight information
                flight_number TEXT NOT NULL UNIQUE,
                flight_date TEXT NOT NULL,
                pilot TEXT,

                -- Aircraft
                manufacturer TEXT,
                model TEXT,
                aircraft TEXT,
                speed REAL NOT NULL,
                fuel_price REAL NOT NULL,

                -- Departure
                departure_code TEXT,
                departure_city TEXT,

                -- Arrival
                arrival_code TEXT,
                arrival_city TEXT,

                -- Compatibility route fields
                departure TEXT,
                arrival TEXT,

                -- Flight calculations
                distance REAL NOT NULL,
                flight_time REAL NOT NULL,
                fuel_needed REAL NOT NULL,
                fuel_consumption REAL,
                fuel_cost REAL NOT NULL,

                -- Flight status
                status TEXT NOT NULL,

                -- Weather Intelligence
                wind_speed REAL,
                wind_direction TEXT,
                temperature REAL,
                pressure REAL,
                humidity REAL,
                visibility REAL,
                weather_condition TEXT,
                weather_severity TEXT,
                weather_factor REAL NOT NULL DEFAULT 1.0
            )
        """)

        # ==================================================
        # VALIDATE VERSION
        # ==================================================

        if current_version > CURRENT_SCHEMA_VERSION:

            raise RuntimeError(
                "The database schema version "
                f"({current_version}) is newer than the "
                f"application-supported version "
                f"({CURRENT_SCHEMA_VERSION}). "
                "Upgrade AeroFlight Suite before opening "
                "this database."
            )

        # ==================================================
        # VERSION 1
        # ==================================================

        if current_version < 1:

            existing_columns = _get_existing_columns(cursor)

            _migrate_to_version_1(
                cursor,
                existing_columns,
            )

            current_version = 1

            cursor.execute("PRAGMA user_version = 1")

        # ==================================================
        # VERSION 2
        # ==================================================

        if current_version < 2:

            existing_columns = _get_existing_columns(cursor)

            _migrate_to_version_2(
                cursor,
                existing_columns,
            )

            current_version = 2

            cursor.execute("PRAGMA user_version = 2")

        # ==================================================
        # VERSION 3
        # ==================================================

        if current_version < 3:

            _migrate_to_version_3(cursor)

            current_version = 3

            cursor.execute("PRAGMA user_version = 3")

        # ==================================================
        # VERSION 4
        # ==================================================

        if current_version < 4:

            _migrate_to_version_4(cursor)

            current_version = 4

            cursor.execute("PRAGMA user_version = 4")

        # ==================================================
        # VERSION 5
        # ==================================================

        if current_version < 5:

            _migrate_to_version_5(cursor)

            current_version = 5

            cursor.execute("PRAGMA user_version = 5")

        # ==================================================
        # PHYSICAL SCHEMA VERIFICATION
        # ==================================================
        #
        # IMPORTANT:
        #
        # Schema repair happens AFTER the official
        # versioned migration chain.
        #
        # It is a safety layer, not a replacement for
        # migrations.
        # ==================================================

        existing_columns = _get_existing_columns(cursor)

        _ensure_current_schema(
            cursor,
            existing_columns,
        )

        # ==================================================
        # LEGACY ROUTE NORMALIZATION
        # ==================================================

        _normalize_route_fields(cursor)

        # ==================================================
        # INDEXES
        # ==================================================

        _create_indexes(cursor)

        # ==================================================
        # VERSION 5 RUNWAY REFERENCE DATA
        # ==================================================
        #
        # Synchronize the static runway reference dataset
        # with the SQLite runway table.
        #
        # Missing reference runways are inserted.
        #
        # Existing database runways are preserved.
        #
        # This operation is intentionally idempotent.
        # ==================================================

        _seed_runway_reference_data(cursor)

        # ==================================================
        # FINAL VERSION CHECKPOINT
        # ==================================================

        cursor.execute(f"PRAGMA user_version = " f"{CURRENT_SCHEMA_VERSION}")

        # ==================================================
        # COMMIT
        # ==================================================

        connection.commit()


# ==========================================================
# SCHEMA HELPERS
# ==========================================================


def _get_existing_columns(cursor):
    """
    Return the current columns of the flights table.

    Returns
    -------
    set[str]
        Existing column names.
    """

    return {row[1] for row in cursor.execute("PRAGMA table_info(flights)")}


def _add_missing_columns(
    cursor,
    existing_columns,
    migrations,
):
    """
    Add missing columns safely.

    Parameters
    ----------
    cursor : sqlite3.Cursor
        Active database cursor.

    existing_columns : set[str]
        Existing database columns.

    migrations : dict
        Mapping between column names and ALTER TABLE
        statements.
    """

    for column, statement in migrations.items():

        if column not in existing_columns:

            cursor.execute(statement)

            existing_columns.add(column)


def _ensure_current_schema(
    cursor,
    existing_columns,
):
    """
    Verify that the current database contains every column
    required by the official AeroFlight Suite V4 schema.

    This function is a safety layer.

    It protects against databases where:

        PRAGMA user_version

    reports the expected version while the physical table
    is incomplete.

    Existing data is preserved.

    Missing columns are added only when necessary.
    """

    required_columns = {
        # --------------------------------------------------
        # Flight
        # --------------------------------------------------
        "pilot": """
            ALTER TABLE flights
            ADD COLUMN pilot TEXT
        """,
        # --------------------------------------------------
        # Aircraft
        # --------------------------------------------------
        "manufacturer": """
            ALTER TABLE flights
            ADD COLUMN manufacturer TEXT
        """,
        "model": """
            ALTER TABLE flights
            ADD COLUMN model TEXT
        """,
        "aircraft": """
            ALTER TABLE flights
            ADD COLUMN aircraft TEXT
        """,
        "speed": """
            ALTER TABLE flights
            ADD COLUMN speed REAL
        """,
        "fuel_price": """
            ALTER TABLE flights
            ADD COLUMN fuel_price REAL
        """,
        # --------------------------------------------------
        # Airports
        # --------------------------------------------------
        "departure_code": """
            ALTER TABLE flights
            ADD COLUMN departure_code TEXT
        """,
        "departure_city": """
            ALTER TABLE flights
            ADD COLUMN departure_city TEXT
        """,
        "arrival_code": """
            ALTER TABLE flights
            ADD COLUMN arrival_code TEXT
        """,
        "arrival_city": """
            ALTER TABLE flights
            ADD COLUMN arrival_city TEXT
        """,
        # --------------------------------------------------
        # Compatibility route fields
        # --------------------------------------------------
        "departure": """
            ALTER TABLE flights
            ADD COLUMN departure TEXT
        """,
        "arrival": """
            ALTER TABLE flights
            ADD COLUMN arrival TEXT
        """,
        # --------------------------------------------------
        # Fuel
        # --------------------------------------------------
        "fuel_needed": """
            ALTER TABLE flights
            ADD COLUMN fuel_needed REAL
        """,
        "fuel_consumption": """
            ALTER TABLE flights
            ADD COLUMN fuel_consumption REAL
        """,
        # --------------------------------------------------
        # Weather
        # --------------------------------------------------
        "wind_speed": """
            ALTER TABLE flights
            ADD COLUMN wind_speed REAL
        """,
        "wind_direction": """
            ALTER TABLE flights
            ADD COLUMN wind_direction TEXT
        """,
        "temperature": """
            ALTER TABLE flights
            ADD COLUMN temperature REAL
        """,
        "pressure": """
            ALTER TABLE flights
            ADD COLUMN pressure REAL
        """,
        "humidity": """
            ALTER TABLE flights
            ADD COLUMN humidity REAL
        """,
        "visibility": """
            ALTER TABLE flights
            ADD COLUMN visibility REAL
        """,
        "weather_condition": """
            ALTER TABLE flights
            ADD COLUMN weather_condition TEXT
        """,
        "weather_severity": """
            ALTER TABLE flights
            ADD COLUMN weather_severity TEXT
        """,
        "weather_factor": """
            ALTER TABLE flights
            ADD COLUMN weather_factor REAL
            DEFAULT 1.0
        """,
    }

    _add_missing_columns(
        cursor,
        existing_columns,
        required_columns,
    )

    # ------------------------------------------------------
    # Synchronize legacy/current calculated fields.
    # ------------------------------------------------------

    _migrate_legacy_calculations(cursor)

    # ------------------------------------------------------
    # Normalize old route information.
    # ------------------------------------------------------

    _migrate_legacy_routes(cursor)

    # ------------------------------------------------------
    # Normalize aircraft information.
    # ------------------------------------------------------

    _migrate_legacy_aircraft(cursor)

    # ------------------------------------------------------
    # Restore default weather factor.
    # ------------------------------------------------------

    cursor.execute("""
        UPDATE flights

        SET weather_factor = 1.0

        WHERE weather_factor IS NULL
        """)


# ==========================================================
# VERSION 1 MIGRATION
# ==========================================================


def _migrate_to_version_1(
    cursor,
    existing_columns,
):
    """
    Migrate legacy Version 0 databases to Version 1.

    Version 1 introduces the expanded flight structure
    used by the modern AeroFlight architecture.

    Existing columns are preserved.
    """

    migrations = {
        # --------------------------------------------------
        # Flight / Pilot
        # --------------------------------------------------
        "pilot": """
            ALTER TABLE flights
            ADD COLUMN pilot TEXT
        """,
        # --------------------------------------------------
        # Aircraft
        # --------------------------------------------------
        "manufacturer": """
            ALTER TABLE flights
            ADD COLUMN manufacturer TEXT
        """,
        "model": """
            ALTER TABLE flights
            ADD COLUMN model TEXT
        """,
        "aircraft": """
            ALTER TABLE flights
            ADD COLUMN aircraft TEXT
        """,
        "speed": """
            ALTER TABLE flights
            ADD COLUMN speed REAL
        """,
        "fuel_price": """
            ALTER TABLE flights
            ADD COLUMN fuel_price REAL
        """,
        # --------------------------------------------------
        # Normalized departure
        # --------------------------------------------------
        "departure_code": """
            ALTER TABLE flights
            ADD COLUMN departure_code TEXT
        """,
        "departure_city": """
            ALTER TABLE flights
            ADD COLUMN departure_city TEXT
        """,
        # --------------------------------------------------
        # Normalized arrival
        # --------------------------------------------------
        "arrival_code": """
            ALTER TABLE flights
            ADD COLUMN arrival_code TEXT
        """,
        "arrival_city": """
            ALTER TABLE flights
            ADD COLUMN arrival_city TEXT
        """,
        # --------------------------------------------------
        # Compatibility route fields
        # --------------------------------------------------
        "departure": """
            ALTER TABLE flights
            ADD COLUMN departure TEXT
        """,
        "arrival": """
            ALTER TABLE flights
            ADD COLUMN arrival TEXT
        """,
        # --------------------------------------------------
        # Fuel
        # --------------------------------------------------
        "fuel_needed": """
            ALTER TABLE flights
            ADD COLUMN fuel_needed REAL
        """,
        "fuel_consumption": """
            ALTER TABLE flights
            ADD COLUMN fuel_consumption REAL
        """,
        # --------------------------------------------------
        # Weather
        # --------------------------------------------------
        "wind_speed": """
            ALTER TABLE flights
            ADD COLUMN wind_speed REAL
        """,
        "wind_direction": """
            ALTER TABLE flights
            ADD COLUMN wind_direction TEXT
        """,
        "temperature": """
            ALTER TABLE flights
            ADD COLUMN temperature REAL
        """,
        "pressure": """
            ALTER TABLE flights
            ADD COLUMN pressure REAL
        """,
        "humidity": """
            ALTER TABLE flights
            ADD COLUMN humidity REAL
        """,
        "visibility": """
            ALTER TABLE flights
            ADD COLUMN visibility REAL
        """,
        "weather_condition": """
            ALTER TABLE flights
            ADD COLUMN weather_condition TEXT
        """,
        "weather_severity": """
            ALTER TABLE flights
            ADD COLUMN weather_severity TEXT
        """,
        "weather_factor": """
            ALTER TABLE flights
            ADD COLUMN weather_factor REAL DEFAULT 1.0
        """,
    }

    _add_missing_columns(
        cursor,
        existing_columns,
        migrations,
    )

    # ------------------------------------------------------
    # Legacy data migration
    # ------------------------------------------------------

    _migrate_legacy_calculations(cursor)

    _migrate_legacy_routes(cursor)

    _migrate_legacy_aircraft(cursor)


# ==========================================================
# VERSION 2 MIGRATION
# ==========================================================


def _migrate_to_version_2(
    cursor,
    existing_columns,
):
    """
    Finalize the AeroFlight Suite V4 schema.

    Version 2 acts as the explicit schema baseline for
    the current V4 architecture.

    The migration is intentionally idempotent:
    running it against an already-upgraded database is safe.

    This protects databases that were created with older
    development versions but were incorrectly marked with
    an outdated schema version.
    """

    migrations = {
        # --------------------------------------------------
        # V4 flight fields
        # --------------------------------------------------
        "pilot": """
            ALTER TABLE flights
            ADD COLUMN pilot TEXT
        """,
        "manufacturer": """
            ALTER TABLE flights
            ADD COLUMN manufacturer TEXT
        """,
        "model": """
            ALTER TABLE flights
            ADD COLUMN model TEXT
        """,
        "aircraft": """
            ALTER TABLE flights
            ADD COLUMN aircraft TEXT
        """,
        "speed": """
            ALTER TABLE flights
            ADD COLUMN speed REAL
        """,
        "fuel_price": """
            ALTER TABLE flights
            ADD COLUMN fuel_price REAL
        """,
        "fuel_needed": """
            ALTER TABLE flights
            ADD COLUMN fuel_needed REAL
        """,
        # --------------------------------------------------
        # Normalized airport fields
        # --------------------------------------------------
        "departure_code": """
            ALTER TABLE flights
            ADD COLUMN departure_code TEXT
        """,
        "departure_city": """
            ALTER TABLE flights
            ADD COLUMN departure_city TEXT
        """,
        "arrival_code": """
            ALTER TABLE flights
            ADD COLUMN arrival_code TEXT
        """,
        "arrival_city": """
            ALTER TABLE flights
            ADD COLUMN arrival_city TEXT
        """,
        # --------------------------------------------------
        # Weather intelligence fields
        # --------------------------------------------------
        "visibility": """
            ALTER TABLE flights
            ADD COLUMN visibility REAL
        """,
        "weather_condition": """
            ALTER TABLE flights
            ADD COLUMN weather_condition TEXT
        """,
        "weather_severity": """
            ALTER TABLE flights
            ADD COLUMN weather_severity TEXT
        """,
        "weather_factor": """
            ALTER TABLE flights
            ADD COLUMN weather_factor REAL DEFAULT 1.0
        """,
    }

    _add_missing_columns(
        cursor,
        existing_columns,
        migrations,
    )

    # ------------------------------------------------------
    # Complete missing legacy values
    # ------------------------------------------------------

    _migrate_legacy_calculations(cursor)

    _migrate_legacy_routes(cursor)

    _migrate_legacy_aircraft(cursor)

    # ------------------------------------------------------
    # Weather defaults
    # ------------------------------------------------------

    cursor.execute("""
        UPDATE flights
        SET weather_factor = 1.0
        WHERE weather_factor IS NULL
        """)


# ==========================================================
# VERSION 3 MIGRATION
# ==========================================================


def _migrate_to_version_3(cursor):
    """
    Bring Version 2 databases to the V4 consistency baseline.

    Version 3 does not introduce a new public column.

    It repairs values that may be incomplete in databases
    created during the intermediate V4 development stage.

    The migration is intentionally idempotent.
    """

    # ------------------------------------------------------
    # Synchronize legacy/current calculation fields.
    # ------------------------------------------------------

    _migrate_legacy_calculations(cursor)

    # ------------------------------------------------------
    # Restore the default weather factor when missing.
    # ------------------------------------------------------

    cursor.execute("""
        UPDATE flights

        SET weather_factor = 1.0

        WHERE weather_factor IS NULL
        """)


# ==========================================================
# VERSION 4 MIGRATION
# ==========================================================


def _migrate_to_version_4(cursor):
    """
    Finalize the AeroFlight Suite V4 schema migration.

    V4 uses the centralized schema verification layer
    to guarantee that every required V4 column exists.

    The actual physical schema repair is intentionally
    centralized in ``_ensure_current_schema()``.

    This prevents V4 from maintaining a second, duplicated
    list of schema columns.

    Important
    ---------
    Legacy columns are NOT deleted.

    In particular, the following compatibility fields
    remain preserved:

        departure
        arrival
        fuel_consumption

    Existing data is therefore retained.

    The migration only prepares the database to reach the
    V4 schema checkpoint. The final physical verification
    is performed by ``create_database()`` after the complete
    versioned migration chain.

    Parameters
    ----------
    cursor : sqlite3.Cursor
        Active database cursor.

    Returns
    -------
    None
    """

    # ======================================================
    # V4 SCHEMA RESPONSIBILITY
    # ======================================================
    #
    # The physical V4 schema is centralized in:
    #
    #     _ensure_current_schema()
    #
    # create_database() calls that function immediately
    # after all versioned migrations.
    #
    # Therefore V4 does not maintain a duplicated list of
    # ALTER TABLE statements.
    #
    # No columns are removed.
    # No existing data is overwritten here.
    # ======================================================

    return None


# ==========================================================
# VERSION 5 MIGRATION
# ==========================================================


def _migrate_to_version_5(cursor):
    """
    Migrate AeroFlight Suite V4 databases to Version 5.

    Version 5 introduces the foundation for runway
    performance management.

    New tables:
        - runways
        - flight_runway_performance

    Existing V4 flight data is preserved.

    The migration is idempotent and safe to execute
    against an already-migrated database.
    """

    # ======================================================
    # RUNWAYS
    # ======================================================
    #
    # Stores runway information independently from flights.
    #
    # No existing flights table data is modified here.
    # ======================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS runways (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            airport_code TEXT NOT NULL,

            runway_id TEXT NOT NULL,

            length REAL,

            width REAL,

            surface TEXT,

            elevation REAL,

            heading REAL,

            UNIQUE (
                airport_code,
                runway_id
            )
        )
    """)

    # ======================================================
    # FLIGHT RUNWAY PERFORMANCE
    # ======================================================
    #
    # Stores runway performance calculations associated
    # with a flight.
    # ======================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS flight_runway_performance (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            flight_id INTEGER NOT NULL,

            runway_id INTEGER,

            airport_code TEXT,

            required_takeoff_distance REAL,

            required_landing_distance REAL,

            takeoff_margin REAL,

            landing_margin REAL,

            takeoff_status TEXT,

            landing_status TEXT,

            temperature REAL,

            aircraft_weight REAL,

            reference_weight REAL,

            FOREIGN KEY (
                flight_id
            )
            REFERENCES flights(id),

            FOREIGN KEY (
                runway_id
            )
            REFERENCES runways(id)
        )
    """)

    # ======================================================
    # V5 INDEXES
    # ======================================================

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS
        idx_runways_airport_code

        ON runways(airport_code)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS
        idx_runways_runway_id

        ON runways(runway_id)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS
        idx_runway_performance_flight_id

        ON flight_runway_performance(flight_id)
    """)

    cursor.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS
        uq_runway_performance_flight_id

        ON flight_runway_performance(flight_id)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS
        idx_runway_performance_airport_code

        ON flight_runway_performance(airport_code)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS
        idx_runway_performance_runway_id

        ON flight_runway_performance(runway_id)
    """)


# ==========================================================
# RUNWAY INSERTION
# ==========================================================


def insert_runway(
    *,
    airport_code,
    runway_id,
    length,
    width=None,
    surface=None,
    elevation=None,
    heading=None,
):
    """Insert or update one runway reference record."""

    if not airport_code:
        raise ValueError("Airport code is required.")

    if not runway_id:
        raise ValueError("Runway ID is required.")

    if length is None:
        raise ValueError("Runway length is required.")

    try:
        normalized_length = float(length)
    except (TypeError, ValueError) as error:
        raise ValueError("Runway length must be numeric.") from error

    if normalized_length <= 0:
        raise ValueError("Runway length must be greater than zero.")

    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO runways (
                airport_code,
                runway_id,
                length,
                width,
                surface,
                elevation,
                heading
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(airport_code, runway_id) DO UPDATE SET
                length = excluded.length,
                width = excluded.width,
                surface = excluded.surface,
                elevation = excluded.elevation,
                heading = excluded.heading
        """,
            (
                str(airport_code).strip().upper(),
                str(runway_id).strip().upper(),
                normalized_length,
                width,
                str(surface).strip() if surface is not None else None,
                elevation,
                heading,
            ),
        )
        return cursor.rowcount


# ==========================================================
# LEGACY DATA MIGRATION
# ==========================================================


def _migrate_legacy_calculations(cursor):
    """
    Normalize legacy flight calculation fields.

    Fuel contract
    -------------
    ``fuel_needed`` is the canonical field.

    ``fuel_consumption`` is retained as a legacy compatibility
    mirror.

    Migration rules
    ---------------
    1. If fuel_needed exists, it wins.
    2. If fuel_needed is NULL but fuel_consumption exists,
       copy fuel_consumption into fuel_needed.
    3. After fuel_needed is available, synchronize
       fuel_consumption with it.
    4. Existing records are never deleted.

    This makes old and new databases follow the same
    application-level fuel contract.

    Parameters
    ----------
    cursor : sqlite3.Cursor
        Active database cursor.

    Returns
    -------
    None
    """

    # ======================================================
    # STEP 1
    # Restore canonical fuel_needed from legacy data
    # when necessary.
    # ======================================================

    cursor.execute("""
        UPDATE flights

        SET fuel_needed = fuel_consumption

        WHERE
            fuel_needed IS NULL
            AND fuel_consumption IS NOT NULL
        """)

    # ======================================================
    # STEP 2
    # Synchronize the legacy mirror.
    #
    # fuel_needed is authoritative.
    # ======================================================

    cursor.execute("""
        UPDATE flights

        SET fuel_consumption = fuel_needed

        WHERE
            fuel_needed IS NOT NULL
            AND (
                fuel_consumption IS NULL
                OR fuel_consumption != fuel_needed
            )
        """)


def _migrate_legacy_routes(cursor):
    """
    Convert legacy route strings such as:

        RBA - Rabat
        MAD - Madrid

    into normalized fields:

        departure_code
        departure_city
        arrival_code
        arrival_city

    Existing normalized values are never overwritten.
    """

    rows = cursor.execute("""
        SELECT
            id,
            departure,
            arrival
        FROM flights
        """).fetchall()

    for row in rows:

        flight_id = row[0]
        departure = row[1]
        arrival = row[2]

        departure_code = None
        departure_city = None

        arrival_code = None
        arrival_city = None

        # --------------------------------------------------
        # Departure
        # --------------------------------------------------

        if departure:

            parts = departure.split(
                " - ",
                1,
            )

            if len(parts) == 2:

                departure_code = parts[0].strip()
                departure_city = parts[1].strip()

            else:

                departure_code = departure.strip()

        # --------------------------------------------------
        # Arrival
        # --------------------------------------------------

        if arrival:

            parts = arrival.split(
                " - ",
                1,
            )

            if len(parts) == 2:

                arrival_code = parts[0].strip()
                arrival_city = parts[1].strip()

            else:

                arrival_code = arrival.strip()

        # --------------------------------------------------
        # Preserve existing values
        # --------------------------------------------------

        cursor.execute(
            """
            UPDATE flights

            SET

                departure_code = COALESCE(
                    departure_code,
                    ?
                ),

                departure_city = COALESCE(
                    departure_city,
                    ?
                ),

                arrival_code = COALESCE(
                    arrival_code,
                    ?
                ),

                arrival_city = COALESCE(
                    arrival_city,
                    ?
                )

            WHERE id = ?
            """,
            (
                departure_code,
                departure_city,
                arrival_code,
                arrival_city,
                flight_id,
            ),
        )


def _migrate_legacy_aircraft(cursor):
    """
    Normalize legacy aircraft data.

    Legacy databases may contain only the combined aircraft
    representation, for example:

        Boeing 777-300ER
        Airbus A320
        ATR ATR 42-600

    The current AeroFlight Suite schema stores aircraft data
    in three synchronized fields:

        manufacturer
        model
        aircraft

    This migration uses the canonical aircraft catalog from
    data.aircraft_data instead of guessing the manufacturer
    or model from the aircraft string.

    Existing valid manufacturer/model values are preserved
    whenever possible.

    Unknown aircraft names are not guessed. They are only
    normalized with TRIM().
    """

    # ------------------------------------------------------
    # Load the canonical aircraft catalog
    # ------------------------------------------------------

    from data.aircraft_data import aircrafts

    # ------------------------------------------------------
    # Build a canonical lookup table
    #
    # Example:
    #
    # "boeing 777-300er"
    #     ->
    # {
    #     "manufacturer": "Boeing",
    #     "model": "777-300ER",
    #     "aircraft": "Boeing 777-300ER"
    # }
    # ------------------------------------------------------

    aircraft_catalog = {}

    for aircraft_data in aircrafts.values():

        manufacturer = str(
            aircraft_data.get(
                "manufacturer",
                "",
            )
        ).strip()

        model = str(
            aircraft_data.get(
                "model",
                "",
            )
        ).strip()

        if not manufacturer or not model:
            continue

        canonical_aircraft = (f"{manufacturer} {model}").strip()

        aircraft_catalog[canonical_aircraft.lower()] = {
            "manufacturer": manufacturer,
            "model": model,
            "aircraft": canonical_aircraft,
            "speed": aircraft_data.get("speed"),
            "fuel_consumption": aircraft_data.get("fuel_consumption"),
        }

    # ------------------------------------------------------
    # Read existing aircraft records
    # ------------------------------------------------------

    rows = cursor.execute("""
        SELECT
            id,
            aircraft,
            manufacturer,
            model,
            speed,
            fuel_consumption
        FROM flights
        """).fetchall()

    # ------------------------------------------------------
    # Normalize each flight
    # ------------------------------------------------------

    for row in rows:

        flight_id = row[0]
        aircraft_value = row[1]
        manufacturer_value = row[2]
        model_value = row[3]
        speed_value = row[4]
        fuel_consumption_value = row[5]

        # --------------------------------------------------
        # Normalize raw aircraft value
        # --------------------------------------------------

        if aircraft_value is None:
            normalized_aircraft = ""
        else:
            normalized_aircraft = str(aircraft_value).strip()

        if not normalized_aircraft:
            continue

        # --------------------------------------------------
        # Try exact match against the canonical catalog
        # --------------------------------------------------

        catalog_entry = aircraft_catalog.get(normalized_aircraft.lower())

        if catalog_entry is not None:

            # --------------------------------------------------
            # Canonical aircraft data
            # --------------------------------------------------

            manufacturer = catalog_entry["manufacturer"]

            model = catalog_entry["model"]

            canonical_aircraft = catalog_entry["aircraft"]

            # --------------------------------------------------
            # Preserve existing speed/fuel values.
            #
            # Only fill missing legacy values from the
            # canonical catalog.
            # --------------------------------------------------

            speed = speed_value if speed_value is not None else catalog_entry["speed"]

            fuel_consumption = (
                fuel_consumption_value
                if fuel_consumption_value is not None
                else catalog_entry["fuel_consumption"]
            )

            cursor.execute(
                """
                UPDATE flights

                SET
                    manufacturer = COALESCE(
                        NULLIF(TRIM(manufacturer), ''),
                        ?
                    ),

                    model = COALESCE(
                        NULLIF(TRIM(model), ''),
                        ?
                    ),

                    aircraft = ?,

                    speed = COALESCE(
                        speed,
                        ?
                    ),

                    fuel_consumption = COALESCE(
                        fuel_consumption,
                        ?
                    )

                WHERE id = ?
                """,
                (
                    manufacturer,
                    model,
                    canonical_aircraft,
                    speed,
                    fuel_consumption,
                    flight_id,
                ),
            )

            continue

        # --------------------------------------------------
        # Unknown aircraft
        # --------------------------------------------------
        #
        # Do NOT guess manufacturer/model.
        #
        # We only normalize the existing aircraft string
        # and preserve existing manufacturer/model values.
        # --------------------------------------------------

        cursor.execute(
            """
            UPDATE flights

            SET
                aircraft = TRIM(aircraft),

                manufacturer = CASE
                    WHEN manufacturer IS NOT NULL
                         AND TRIM(manufacturer) != ''
                    THEN TRIM(manufacturer)
                    ELSE manufacturer
                END,

                model = CASE
                    WHEN model IS NOT NULL
                         AND TRIM(model) != ''
                    THEN TRIM(model)
                    ELSE model
                END

            WHERE id = ?
            """,
            (flight_id,),
        )


# ==========================================================
# ROUTE NORMALIZATION
# ==========================================================


def _normalize_route_fields(cursor):
    """
    Keep compatibility departure/arrival fields synchronized
    with the normalized airport fields.

    Canonical format:

        CODE - CITY
    """

    cursor.execute("""
        UPDATE flights

        SET

            departure = CASE

                WHEN departure_code IS NOT NULL
                     AND TRIM(departure_code) != ''
                     AND departure_city IS NOT NULL
                     AND TRIM(departure_city) != ''

                THEN
                    TRIM(departure_code)
                    || ' - '
                    || TRIM(departure_city)

                WHEN departure_code IS NOT NULL
                     AND TRIM(departure_code) != ''

                THEN
                    TRIM(departure_code)

                WHEN departure_city IS NOT NULL
                     AND TRIM(departure_city) != ''

                THEN
                    TRIM(departure_city)

                ELSE departure

            END,

            arrival = CASE

                WHEN arrival_code IS NOT NULL
                     AND TRIM(arrival_code) != ''
                     AND arrival_city IS NOT NULL
                     AND TRIM(arrival_city) != ''

                THEN
                    TRIM(arrival_code)
                    || ' - '
                    || TRIM(arrival_city)

                WHEN arrival_code IS NOT NULL
                     AND TRIM(arrival_code) != ''

                THEN
                    TRIM(arrival_code)

                WHEN arrival_city IS NOT NULL
                     AND TRIM(arrival_city) != ''

                THEN
                    TRIM(arrival_city)

                ELSE arrival

            END
        """)


# ==========================================================
# INDEXES
# ==========================================================


def _create_indexes(cursor):
    """
    Create indexes used by the current database API.

    IF NOT EXISTS makes this operation safe to execute
    every time the application starts.
    """

    cursor.executescript("""
        CREATE INDEX IF NOT EXISTS idx_flight_number
        ON flights(flight_number);

        CREATE INDEX IF NOT EXISTS idx_departure_code
        ON flights(departure_code);

        CREATE INDEX IF NOT EXISTS idx_departure_city
        ON flights(departure_city);

        CREATE INDEX IF NOT EXISTS idx_arrival_code
        ON flights(arrival_code);

        CREATE INDEX IF NOT EXISTS idx_arrival_city
        ON flights(arrival_city);

        CREATE INDEX IF NOT EXISTS idx_departure
        ON flights(departure);

        CREATE INDEX IF NOT EXISTS idx_arrival
        ON flights(arrival);

        CREATE INDEX IF NOT EXISTS idx_aircraft
        ON flights(aircraft);

        CREATE INDEX IF NOT EXISTS idx_flight_date
        ON flights(flight_date);

        CREATE INDEX IF NOT EXISTS idx_status
        ON flights(status);

        CREATE INDEX IF NOT EXISTS idx_weather_factor
        ON flights(weather_factor);

        CREATE INDEX IF NOT EXISTS idx_runways_airport_code
        ON runways(airport_code);

        CREATE INDEX IF NOT EXISTS idx_runways_runway_id
        ON runways(runway_id);

        CREATE INDEX IF NOT EXISTS idx_runway_performance_flight_id
        ON flight_runway_performance(flight_id);

        CREATE UNIQUE INDEX IF NOT EXISTS uq_runway_performance_flight_id
        ON flight_runway_performance(flight_id);

        CREATE INDEX IF NOT EXISTS idx_runway_performance_airport_code
        ON flight_runway_performance(airport_code);

        CREATE INDEX IF NOT EXISTS idx_runway_performance_runway_id
        ON flight_runway_performance(runway_id);
        """)


# ==========================================================
# VERSION 5 RUNWAY REFERENCE SEEDING
# ==========================================================


def _seed_runway_reference_data(cursor):
    """
    Seed the SQLite runway reference table from the
    static Version 5 runway dataset.

    Only missing runways are inserted.

    Existing database runway records are preserved so
    manually maintained or previously persisted runway
    data is never overwritten.

    The operation is idempotent and therefore safe to
    execute every time the database is initialized.

    Parameters
    ----------
    cursor : sqlite3.Cursor
        Active database cursor.
    """

    for airport_code, airport_runways in RUNWAY_REFERENCE_DATA.items():

        normalized_airport_code = str(airport_code).strip().upper()

        if not normalized_airport_code:
            continue

        for runway in airport_runways:

            runway_id = runway.get("runway_id")

            if runway_id is None:
                continue

            normalized_runway_id = str(runway_id).strip().upper()

            if not normalized_runway_id:
                continue

            cursor.execute(
                """
                INSERT OR IGNORE INTO runways (
                    airport_code,
                    runway_id,
                    length,
                    width,
                    surface,
                    elevation,
                    heading
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    normalized_airport_code,
                    normalized_runway_id,
                    runway.get("length"),
                    runway.get("width"),
                    runway.get("surface"),
                    runway.get("elevation"),
                    runway.get("heading"),
                ),
            )


# ==========================================================
# INSERT FLIGHT
# ==========================================================


def insert_flight(
    *,
    connection=None,
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
    wind_speed,
    wind_direction,
    temperature,
    pressure,
    humidity,
    visibility,
    weather_condition,
    weather_severity,
    weather_factor,
):
    """
    Insert a complete Flight into the SQLite database.

    Fuel contract
    -------------
    ``fuel_needed`` is the canonical flight-level fuel value.

    ``fuel_consumption`` is retained only as a legacy
    compatibility field for historical databases and older
    consumers.

    New flight records always synchronize both fields:

        fuel_needed
            ↓
        fuel_consumption

    This prevents the two columns from containing different
    values for newly created flights.

    Parameters
    ----------
    All parameters are keyword-only.

    Returns
    -------
    int
        ID of the newly inserted flight.
    """

    try:

        # ==================================================
        # NORMALIZE CANONICAL FUEL VALUE
        # ==================================================

        if fuel_needed is None:
            raise ValueError("Fuel needed is required.")

        normalized_fuel_needed = float(fuel_needed)

        if normalized_fuel_needed < 0:
            raise ValueError("Fuel needed cannot be negative.")

        # --------------------------------------------------
        # Legacy compatibility value
        #
        # IMPORTANT:
        # This is NOT an independent calculation.
        #
        # It mirrors fuel_needed for compatibility.
        # --------------------------------------------------

        legacy_fuel_consumption = normalized_fuel_needed

        with (
            nullcontext(connection) if connection is not None else get_connection()
        ) as connection:

            cursor = connection.cursor()

            # ==================================================
            # AIRCRAFT REPRESENTATION
            # ==================================================

            aircraft = (
                f"{manufacturer} {model}".strip() if manufacturer or model else ""
            )

            # ==================================================
            # ROUTE REPRESENTATION
            # ==================================================

            departure = _format_airport(
                departure_code,
                departure_city,
            )

            arrival = _format_airport(
                arrival_code,
                arrival_city,
            )

            # ==================================================
            # INSERT
            # ==================================================

            cursor.execute(
                """
                INSERT INTO flights (

                    flight_number,
                    flight_date,
                    pilot,

                    manufacturer,
                    model,
                    aircraft,

                    departure_code,
                    departure_city,
                    arrival_code,
                    arrival_city,

                    departure,
                    arrival,

                    distance,
                    speed,
                    fuel_price,
                    flight_time,

                    fuel_needed,
                    fuel_consumption,
                    fuel_cost,

                    status,

                    wind_speed,
                    wind_direction,
                    temperature,
                    pressure,
                    humidity,
                    visibility,

                    weather_condition,
                    weather_severity,
                    weather_factor
                )

                VALUES (

                    :flight_number,
                    :flight_date,
                    :pilot,

                    :manufacturer,
                    :model,
                    :aircraft,

                    :departure_code,
                    :departure_city,
                    :arrival_code,
                    :arrival_city,

                    :departure,
                    :arrival,

                    :distance,
                    :speed,
                    :fuel_price,
                    :flight_time,

                    :fuel_needed,
                    :fuel_consumption,
                    :fuel_cost,

                    :status,

                    :wind_speed,
                    :wind_direction,
                    :temperature,
                    :pressure,
                    :humidity,
                    :visibility,

                    :weather_condition,
                    :weather_severity,
                    :weather_factor
                )
                """,
                {
                    "flight_number": flight_number,
                    "flight_date": flight_date,
                    "pilot": pilot,
                    "manufacturer": manufacturer,
                    "model": model,
                    "aircraft": aircraft,
                    "departure_code": departure_code,
                    "departure_city": departure_city,
                    "arrival_code": arrival_code,
                    "arrival_city": arrival_city,
                    "departure": departure,
                    "arrival": arrival,
                    "distance": distance,
                    "speed": speed,
                    "fuel_price": fuel_price,
                    "flight_time": flight_time,
                    # Canonical value.
                    "fuel_needed": normalized_fuel_needed,
                    # Legacy compatibility mirror.
                    "fuel_consumption": legacy_fuel_consumption,
                    "fuel_cost": fuel_cost,
                    "status": status,
                    "wind_speed": wind_speed,
                    "wind_direction": wind_direction,
                    "temperature": temperature,
                    "pressure": pressure,
                    "humidity": humidity,
                    "visibility": visibility,
                    "weather_condition": weather_condition,
                    "weather_severity": weather_severity,
                    "weather_factor": weather_factor,
                },
            )

            return cursor.lastrowid

    except sqlite3.IntegrityError as error:

        if "flight_number" in str(error).lower():

            raise ValueError(
                f"Flight number '{flight_number}' already exists."
            ) from error

        raise ValueError(
            f"Could not insert flight " f"'{flight_number}': {error}"
        ) from error

    except sqlite3.Error as error:

        raise RuntimeError(
            f"Database error while inserting flight " f"'{flight_number}': {error}"
        ) from error


# ==========================================================
# AIRPORT FORMATTING
# ==========================================================


def _format_airport(
    code,
    city,
):
    """
    Return the canonical airport representation.

    Examples
    --------
    RBA + Rabat
        -> RBA - Rabat

    RBA + empty city
        -> RBA

    empty code + Rabat
        -> Rabat
    """

    normalized_code = str(code).strip() if code is not None else ""

    normalized_city = str(city).strip() if city is not None else ""

    if normalized_code and normalized_city:

        return f"{normalized_code} - " f"{normalized_city}"

    if normalized_code:
        return normalized_code

    return normalized_city
