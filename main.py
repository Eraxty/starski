from astronomy import get_objects
from renderer import render

lat = float(input("Latitude: "))
lon = float(input("Longitude: "))
facing = float(input("Facing (0-359°): "))

objects = get_objects(lat, lon)
render(objects, facing)