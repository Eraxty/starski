from astronomy import get_objects
from renderer import render

lat = float(input("Latitude: "))
lon = float(input("Longitude: "))

objects = get_objects(lat, lon)

render(objects)