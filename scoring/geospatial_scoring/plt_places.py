import requests
from geopy.distance import geodesic
import matplotlib.pyplot as plt

# Address and Nominatim API URL
address = "Dominikanerinnenplatz 11b und Jean-Spessart-Str. 7 Euskirchen (53879)"
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
    location_data = []
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
        
        # Create a set to check types
        seen_types = {}
        
        # Lists for plotting
        plot_latitudes = []
        plot_longitudes = []
        plot_types = []
    
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
                place_type = "Fast food"
            elif place.get("tags", {}).get("amenity") == "ice_cream":
                place_type = "Ice Cream"
            elif place.get("tags", {}).get("building") == "supermarket":
                place_type = "market2"        
            elif place.get("tags", {}).get("leisure") == "garden":
                place_type = "garden"
            elif place.get("tags", {}).get("place") == "square":
                place_type = "Square"
            elif place.get("tags", {}).get("amenity") == "library":
                place_type = "library"
            elif place.get("tags", {}).get("amenity") == "pharmacy":
                place_type = "pharmacy"
            elif place.get("tags", {}).get("shop") == "cosmetics":
                place_type = "cosmetics"
            elif place.get("tags", {}).get("amenity") == "school":
                place_type = "school"
            elif place.get("tags", {}).get("amenity") == "kindergarten":
                place_type = "kindergarten"
            elif place.get("tags", {}).get("amenity") == "university":
                place_type = "university"
            elif place.get("tags", {}).get("landuse") == "education":
                place_type = "education"
            elif place.get("tags", {}).get("education") == "centre":
                place_type = "centre"
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
                
                # Add to plot lists
                plot_latitudes.append(place["lat"])
                plot_longitudes.append(place["lon"])
                plot_types.append(place_type)

                seen_types[place_type] = True  # Mark this type of place as already listed
                
        # Plotting
        plt.figure(figsize=(10, 8))
        plt.scatter(plot_longitudes, plot_latitudes, c='blue', alpha=0.5, edgecolors='k')
        plt.title('Nearby Locations')
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        
        # Annotate each point with its type
        for i, place_type in enumerate(plot_types):
            plt.annotate(place_type, (plot_longitudes[i], plot_latitudes[i]), fontsize=9, ha='right')
        
        plt.scatter(lon, lat, c='red', label='Your Location', s=100)  # Plot your location
        plt.legend()
        plt.grid()
        plt.show()

    else:
        print("Nearby locations API call failed.")
        print(f"Response content: {overpass_response.text}")

else:
    print("Address not found or invalid. Please check the address.")
