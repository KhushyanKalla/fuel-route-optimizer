import os
import requests

ORS_API_KEY = os.environ.get('ORS_API_KEY')

def geocode_city(city_name):
    
    url = "https://api.openrouteservice.org/geocode/search"
    
    params = {
        'api_key' : ORS_API_KEY,
        'text' : city_name,
        'boundary.country' : 'US',
        'size' : 1
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    if not data['features'] :
        raise ValueError(f"city not found {city_name}")
    coords = data['features'][0]['geometry']['coordinates']
    return (coords[1], coords[0])


def get_route(start_city, end_city):
    start_coords = geocode_city(start_city)
    end_coords = geocode_city(end_city)
    
    # Get Route from the Ors
    url = "https://api.openrouteservice.org/v2/directions/driving-car"
    
    headers = {
        'Authorization': ORS_API_KEY,
        'Content-Type': 'application/json'
    }
    body = {
        "coordinates": [
            [start_coords[1], start_coords[0]], 
            [end_coords[1], end_coords[0]]
        ]
    }
    
    response = requests.post(url, json=body, headers=headers)
    data = response.json()
    
    
    route = data['routes'][0]
    
    # Distance comes in meters, convert to miles
    distance_miles = route['summary']['distance'] / 1609.34
    
    geometry = route['geometry']
    
    coordinates = decode_polyline(geometry)
    coordinates = decode_polyline(geometry)
    
    return {
        'start': start_city,
        'end': end_city,
        'distance_miles': round(distance_miles, 2),
        'coordinates': coordinates,
        'start_coords': start_coords,
        'end_coords': end_coords
    }


def decode_polyline(polyline_str):

    index = 0
    lat = 0
    lng = 0
    coordinates = []
    changes = {'latitude': 0, 'longitude': 0}

    while index < len(polyline_str):
        for unit in ['latitude', 'longitude']:
            shift = 0
            result = 0

            while True:
                byte = ord(polyline_str[index]) - 63
                index += 1
                result |= (byte & 0x1f) << shift
                shift += 5
                if not byte >= 0x20:
                    break

            if result & 1:
                changes[unit] = ~(result >> 1)
            else:
                changes[unit] = result >> 1

        lat += changes['latitude']
        lng += changes['longitude']
        coordinates.append((lat / 100000.0, lng / 100000.0))

    return coordinates