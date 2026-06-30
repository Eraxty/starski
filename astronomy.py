from skyfield.api import load, wgs84, Star
from skyfield.data import hipparcos
from models import obj

# Load data
planets = load("de421.bsp")
ts = load.timescale()
earth = planets["earth"]

# Objects
OBJECTS = {
    "Sun": ("sun", "☀"),
    "Moon": ("moon", "☾"),
    "Mercury": ("mercury", "☿"),
    "Venus": ("venus", "♀"),
    "Mars": ("mars", "♂"),
    "Jupiter": ("jupiter barycenter", "♃"),
    "Saturn": ("saturn barycenter", "♄"),
}

# Load Hipparcos star catalog
with load.open(hipparcos.URL) as f:
    STAR_CATALOG = hipparcos.load_dataframe(f)

# Only bright stars
STAR_CATALOG = STAR_CATALOG[STAR_CATALOG["magnitude"] <= 4.5]


def get_objects(latitude: float, longitude: float):
    t = ts.now()

    observer = earth + wgs84.latlon(
        latitude_degrees=latitude,
        longitude_degrees=longitude,
    )

    objects = []

    # Planets
    for name, (key, symbol) in OBJECTS.items():
        body = planets[key]

        apparent = observer.at(t).observe(body).apparent()
        alt, az, _ = apparent.altaz()

        objects.append(
            obj(
                name=name,
                altitude=alt.degrees,
                azimuth=az.degrees,
                symbol=symbol,
            )
        )

    # Stars
    for hip_id, row in STAR_CATALOG.iterrows():
        try:
            star = Star.from_dataframe(row)

            apparent = observer.at(t).observe(star).apparent()
            alt, az, _ = apparent.altaz()

            if alt.degrees < 0:
                continue

            objects.append(
                obj(
                    name=f"HIP {hip_id}",
                    altitude=alt.degrees,
                    azimuth=az.degrees,
                    symbol="✦",
                    magnitude=row["magnitude"],
                )
            )

        except Exception as e:
            print(f"Skipping HIP {hip_id}: {e}")
            continue

    return objects