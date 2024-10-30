import requests
from geopy.distance import geodesic

# Adres ve Nominatim API URL'si
address = "Vöhrenbacher Straße 49, Villingen, 78050 Villingen-Schwenningen"
nominatim_url = "https://nominatim.openstreetmap.org/search"

# 1. Adresi koordinatlara dönüştürme (Geocoding)
params = {
    "q": address,
    "format": "json",
    "limit": 1
}
response = requests.get(nominatim_url, params=params)
location_data = response.json()[0] if response.ok and response.json() else None

if location_data:
    lat, lon = float(location_data["lat"]), float(location_data["lon"])
    print(f"Adres koordinatları: Enlem: {lat}, Boylam: {lon}")
    
    # 2. Çevredeki yapıları (tren durakları, marketler) bulma
    overpass_url = "http://overpass-api.de/api/interpreter"
    query = f"""
    [out:json];
    node(around:1000,{lat},{lon})[amenity~"market|station"];
    out;
    """
    overpass_response = requests.get(overpass_url, params={"data": query})
    nearby_locations = overpass_response.json()["elements"] if overpass_response.ok else []

    # 3. Mesafe hesaplama ve puan atama
    for place in nearby_locations:
        place_name = place.get("tags", {}).get("name", "Unnamed")
        place_type = place.get("tags", {}).get("amenity", "Unknown")
        place_coords = (place["lat"], place["lon"])
        distance = geodesic((lat, lon), place_coords).meters
        
        # Puanlama (Örnek olarak mesafeye göre bir ölçek)
        if distance < 500:
            score = 10
        elif distance < 1000:
            score = 7
        elif distance < 2000:
            score = 5
        else:
            score = 2

        print(f"{place_type.capitalize()} - {place_name}: Mesafe {distance:.2f} m, Puan: {score}")
else:
    print("Adres bulunamadı veya geçersiz.")
