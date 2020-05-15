import googlemaps
from datetime import datetime

gmaps = googlemaps.Client(key='AIzaSyAWiHE0okg-Uro_IxRTgGAvpnP1BYe1uJA')

dist = gmaps.distance_matrix("13.3269,77.1261","13.3379,77.1173", mode="driving", language=None, avoid=None, units=None, departure_time=None, arrival_time=None, transit_mode=None, transit_routing_preference=None, traffic_model=None, region=None)
dist=((dist["rows"][0]["elements"][0]["distance"]["value"])/1000)
print(dist)
