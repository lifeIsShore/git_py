import requests
from geopy.distance import geodesic

# Address and Nominatim API URL
address = "yildirim beyazit, Kayseri, Turkey"
nominatim_url = "https://nominatim.openstreetmap.org/search"

# 1. Convert the address to coordinates (Geocoding)
params = {
    "q": address,
    "format": "json",
    "limit": 1
}

# Add User-Agent header
headers = {
    "User-Agent": "MyGeocodingApp/1.0 (myemail@example.com)"  # Put your email address here
}

response = requests.get(nominatim_url, params=params, headers=headers)

# Check the response
try:
    response.raise_for_status()  # Check for HTTP errors
    location_data = response.json()  # Parse the response as JSON
except requests.exceptions.HTTPError as err:
    print(f"Error: {err}")
    print(f"Response content: {response.text}")
except ValueError:
    print("Response is not in JSON format.")
    print(f"Response content: {response.text}")
    location_data = []

# Error checking
if location_data:
    # Get coordinates from the first result
    location_data = location_data[0]
    lat, lon = float(location_data["lat"]), float(location_data["lon"])
    print(f"Address coordinates: Latitude: {lat}, Longitude: {lon}")
    
    # 2. Find nearby markets, bus/train stops, and parks
    overpass_url = "http://overpass-api.de/api/interpreter"
    query = f"""
    [out:json];
    (
      node(around:1000,{lat},{lon})[amenity=market];
      node(around:1000,{lat},{lon})[public_transport=stop_position][bus=yes];
      node(around:1000,{lat},{lon})[railway=station];
      node(around:1000,{lat},{lon})[leisure=park];
    );
    out;
    """
    overpass_response = requests.get(overpass_url, params={"data": query})

    # Check the response
    if overpass_response.ok:
        nearby_locations = overpass_response.json()["elements"]
        
        # Create a set to check types
        seen_types = {}
    
        # 3. Calculate distance and determine type
        for place in nearby_locations:
            # Determine location type
            if place.get("tags", {}).get("amenity") == "market":
                place_type = "Market"
            elif place.get("tags", {}).get("public_transport") == "stop_position" and place.get("tags", {}).get("bus") == "yes":
                place_type = "Bus Stop"
            elif place.get("tags", {}).get("railway") == "station":
                place_type = "Train Station"
            elif place.get("tags", {}).get("leisure") == "park":
                place_type = "Park"
            else:
                place_type = "Unknown"
    
            # If this type of place has not been listed before
            if place_type not in seen_types:
                # Calculate distance
                place_coords = (place["lat"], place["lon"])
                distance = geodesic((lat, lon), place_coords).meters
    
                # Scoring
                if distance < 500:
                    score = 10
                elif distance < 1000:
                    score = 7
                elif distance < 2000:
                    score = 5
                else:
                    score = 2
    
                print(f"{place_type}: Distance {distance:.2f} m, Score: {score}")
                seen_types[place_type] = True  # Mark this type of place as already listed
    else:
        print("Nearby locations API call failed.")
        print(f"Response content: {overpass_response.text}")

else:
    print("Address not found or invalid. Please check the address.")
