from astronomy import get_objects
from renderer import render
import time
import os


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


# Ask once
lat = input_coordinate("Latitude", "N", "S")
lon = input_coordinate("Longitude", "E", "W")
facing = float(input("\nFacing (0-359°): ")) % 360

# Update forever
print("\033[?25l", end="")
try:
    while True:
        objects = get_objects(lat, lon)
        print("\033[2J\033[H", end="")
        render(objects, facing)
        time.sleep(1)

except KeyboardInterrupt:
    pass
finally:
    print("\033[?25h", end="")