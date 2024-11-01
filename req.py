import requests
from geopy.distance import geodesic

# Address and Nominatim API URL
address = "Rottweiler Str. 4, 78056 Villingen-Schwenningen"
nominatim_url = "https://nominatim.openstreetmap.org/search"

# 1. Convert the address to coordinates (Geocoding)
params = {
    "q": address,
    "format": "json",
    "limit": 1
}

# Add User-Agent header
headers = {
    "User-Agent": "MyGeocodingApp/1.0 (meforpresident38@gmail.com)"
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
    
    # 2. Find nearby locations
    overpass_url = "http://overpass-api.de/api/interpreter"
    query = f"""
    [out:json];
    (
      node(around:1000,{lat},{lon})[shop=supermarket];
      node(around:1000,{lat},{lon})[shop=convenience];
      node(around:1000,{lat},{lon})[shop=variety_store];
      node(around:1000,{lat},{lon})[shop=general];
      node(around:1000,{lat},{lon})[shop=greengrocer];
      node(around:1000,{lat},{lon})[shop=department_store];
      node(around:1000,{lat},{lon})[public_transport=stop_position][bus=yes];
      node(around:1000,{lat},{lon})[railway=station];
      node(around:1000,{lat},{lon})[leisure=park];
      node(around:1000,{lat},{lon})[amenity=fast_food];
      node(around:1000,{lat},{lon})[amenity=ice_cream];
      node(around:1000,{lat},{lon})[building=supermarket];
      node(around:1000,{lat},{lon})[leisure=garden];
      node(around:1000,{lat},{lon})[place=square];
      node(around:1000,{lat},{lon})[amenity=library];
      node(around:1000,{lat},{lon})[amenity=pharmacy];
      node(around:1000,{lat},{lon})[shop=cosmetics];
      node(around:1000,{lat},{lon})[amenity=school];
      node(around:1000,{lat},{lon})[amenity=kindergarten];
      node(around:1000,{lat},{lon})[amenity=university];
      node(around:1000,{lat},{lon})[education=centre];
      node(around:1000,{lat},{lon})[landuse=education];
    );
    out;
    """
    overpass_response = requests.get(overpass_url, params={"data": query})

    # Check the response
    if overpass_response.ok:
        nearby_locations = overpass_response.json()["elements"]
        
        # Create dictionaries to track types and last locations
        seen_types = {}
        last_location = {}
        total_score = 0  # Initialize total score

        # 3. Calculate distance and determine type
        for place in nearby_locations:
            # Determine location type
            if place.get("tags", {}).get("shop") == "supermarket":
                place_type = "Supermarket"
            elif place.get("tags", {}).get("shop") == "convenience":
                place_type = "Convenience Store"
            elif place.get("tags", {}).get("shop") == "general":
                place_type = "General Store"
            elif place.get("tags", {}).get("shop") == "variety_store":
                place_type = "Variety Store"
            elif place.get("tags", {}).get("shop") == "greengrocer":
                place_type = "Greengrocer"
            elif place.get("tags", {}).get("shop") == "department_store":
                place_type = "Department Store"
            elif place.get("tags", {}).get("public_transport") == "stop_position" and place.get("tags", {}).get("bus") == "yes":
                place_type = "Bus Stop"
            elif place.get("tags", {}).get("railway") == "station":
                place_type = "Train Station"
            elif place.get("tags", {}).get("amenity") == "fast_food":
                place_type = "Fast Food"
            elif place.get("tags", {}).get("amenity") == "ice_cream":
                place_type = "Ice Cream"
            elif place.get("tags", {}).get("building") == "supermarket":
                place_type = "Market"
            elif place.get("tags", {}).get("leisure") == "garden":
                place_type = "Garden"
            elif place.get("tags", {}).get("place") == "square":
                place_type = "Square"
            elif place.get("tags", {}).get("amenity") == "library":
                place_type = "Library"
            elif place.get("tags", {}).get("amenity") == "pharmacy":
                place_type = "Pharmacy"
            elif place.get("tags", {}).get("shop") == "cosmetics":
                place_type = "Cosmetics Store"
            elif place.get("tags", {}).get("amenity") == "school":
                place_type = "School"
            elif place.get("tags", {}).get("amenity") == "kindergarten":
                place_type = "Kindergarten"
            elif place.get("tags", {}).get("amenity") == "university":
                place_type = "University"
            elif place.get("tags", {}).get("landuse") == "education":
                place_type = "Education Area"
            elif place.get("tags", {}).get("education") == "centre":
                place_type = "Education Centre"
            else:
                place_type = "Unknown"

            # Calculate distance
            place_coords = (place["lat"], place["lon"])
            distance = geodesic((lat, lon), place_coords).meters
            
            # Check distance from last location of the same type
            if place_type in last_location:
                prev_coords = last_location[place_type]
                prev_distance = geodesic(prev_coords, place_coords).meters
            else:
                prev_distance = float("inf")  # No previous location
            
            # Apply distance-based scoring if within 1000 meters and far enough from previous same type
            if distance <= 1000.0 and prev_distance > 90.0:
                if distance <= 200:
                    score = 10
                elif distance <= 500:
                    score = 8
                elif distance <= 750:
                    score = 5
                else:
                    score = 3

                total_score += score  # Add to total score
                print(f"{place_type}: Distance {distance:.2f} m, Score: {score}")
                last_location[place_type] = place_coords  # Update last location for this type
                seen_types[place_type] = True
            elif distance <= 1000:
                print(f"{place_type} within 1000 m but too close to previous same type; skipped.")
            else:
                print(f"{place_type} is more than 1000 m away and will not be scored.")
                
                
        # Print the total score
        print(f"Total Score: {total_score}")

    else:
        print("Nearby locations API call failed.")
        print(f"Response content: {overpass_response.text}")

else:
    print("Address not found or invalid. Please check the address.")
