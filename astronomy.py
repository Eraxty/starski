from skyfield.api import load, wgs84, Star
from skyfield.data import hipparcos
from models import obj
import warnings

warnings.filterwarnings(
    "ignore",
    message="invalid value"
)

# Load data
planets = load("de421.bsp")
ts = load.timescale()
earth = planets["earth"]

# Planets
OBJECTS = {
    "Sun": "sun",
    "Moon": "moon",
    "Mercury": "mercury",
    "Venus": "venus",
    "Mars": "mars",
    "Jupiter": "jupiter barycenter",
    "Saturn": "saturn barycenter",
}

# Important stars
IMPORTANT_STARS = {
    11767: "Polaris",
    24436: "Rigel",
    25336: "Aldebaran",
    27989: "Betelgeuse",
    32349: "Sirius",
    37279: "Procyon",
    65474: "Arcturus",
    69673: "Spica",
    80763: "Antares",
    91262: "Vega",
    97649: "Altair",
    102098: "Deneb",
    113368: "Fomalhaut",
}

# Load Hipparcos catalog
with load.open(hipparcos.URL) as f:
    STAR_CATALOG = hipparcos.load_dataframe(f)

def get_objects(latitude: float, longitude: float):
    t = ts.now()

    observer = earth + wgs84.latlon(
        latitude_degrees=latitude,
        longitude_degrees=longitude,
    )

    objects = []

    # Planets
    for name, key in OBJECTS.items():
        body = planets[key]

        apparent = observer.at(t).observe(body).apparent()
        alt, az, _ = apparent.altaz()

        if alt.degrees < 0:
            continue

        objects.append(
            obj(
                name=name,
                altitude=alt.degrees,
                azimuth=az.degrees,
                type="planet",
            )
        )

    # Stars
    for hip_id, star_name in IMPORTANT_STARS.items():
        try:
            row = STAR_CATALOG.loc[hip_id]
            star = Star.from_dataframe(row)

            apparent = observer.at(t).observe(star).apparent()
            alt, az, _ = apparent.altaz()

            if alt.degrees < 0:
                continue

            objects.append(
                obj(
                    name=star_name,
                    altitude=alt.degrees,
                    azimuth=az.degrees,
                    magnitude=row["magnitude"],
                    type="important_star",
                )
            )

        except Exception:
            continue

    # Other bright stars
    for hip_id, row in STAR_CATALOG.iterrows():

        if hip_id in IMPORTANT_STARS:
            continue

        if row["magnitude"] > 3.5:
            continue

        try:
            star = Star.from_dataframe(row)

            apparent = observer.at(t).observe(star).apparent()
            alt, az, _ = apparent.altaz()

            if alt.degrees < 0:
                continue

            objects.append(
                obj(
                    name="",
                    altitude=alt.degrees,
                    azimuth=az.degrees,
                    magnitude=row["magnitude"],
                    type="star",
                )
            )

        except Exception:
            continue
        
    return objects
