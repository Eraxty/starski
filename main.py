from astronomy import get_objects
from renderer import render


def input_coordinate(name, positive, negative):
    print(f"\n{name}")

    degrees = float(input("Degrees : "))
    minutes = float(input("Minutes : "))
    seconds = float(input("Seconds : "))
    direction = input(f"Direction ({positive}/{negative}): ").strip().upper()

    decimal = degrees + minutes / 60 + seconds / 3600

    if direction == negative:
        decimal *= -1

    return decimal


lat = input_coordinate("Latitude", "N", "S")
lon = input_coordinate("Longitude", "E", "W")
facing = float(input("\nFacing (0-359°): "))

objects = get_objects(lat, lon)
render(objects, facing)