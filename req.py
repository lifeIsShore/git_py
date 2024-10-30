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

# User-Agent başlığı ekle
headers = {
    "User-Agent": "MyGeocodingApp/1.0 (myemail@example.com)"  # Kendi e-posta adresinizi buraya yazın
}

response = requests.get(nominatim_url, params=params, headers=headers)

# Yanıtı kontrol et
try:
    response.raise_for_status()  # HTTP hatalarını kontrol et
    location_data = response.json()  # JSON olarak yanıtı ayrıştır
except requests.exceptions.HTTPError as err:
    print(f"Hata: {err}")
    print(f"Yanıt içeriği: {response.text}")
except ValueError:
    print("Yanıt JSON formatında değil.")
    print(f"Yanıt içeriği: {response.text}")
    location_data = []

# Hata kontrolü
if location_data:
    # İlk sonuçtan koordinatları al
    location_data = location_data[0]
    lat, lon = float(location_data["lat"]), float(location_data["lon"])
    print(f"Adres koordinatları: Enlem: {lat}, Boylam: {lon}")
    
    # 2. Çevredeki marketler, otobüs/tren durakları ve parkları bulma
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

    # Yanıtı kontrol et
    if overpass_response.ok:
        nearby_locations = overpass_response.json()["elements"]
        
        # Türleri kontrol etmek için bir set oluştur
        seen_types = {}
    
        # 3. Mesafe hesaplama ve tür belirleme
        for place in nearby_locations:
            # Konum türünü belirleme
            if place.get("tags", {}).get("amenity") == "market":
                place_type = "Market"
            elif place.get("tags", {}).get("public_transport") == "stop_position" and place.get("tags", {}).get("bus") == "yes":
                place_type = "Otobüs Durağı"
            elif place.get("tags", {}).get("railway") == "station":
                place_type = "Tren Durağı"
            elif place.get("tags", {}).get("leisure") == "park":
                place_type = "Park"
            else:
                place_type = "Bilinmeyen"
    
            # Eğer daha önce bu türde bir yer listelenmemişse
            if place_type not in seen_types:
                # Mesafe hesaplama
                place_coords = (place["lat"], place["lon"])
                distance = geodesic((lat, lon), place_coords).meters
    
                # Puanlama
                if distance < 500:
                    score = 10
                elif distance < 1000:
                    score = 7
                elif distance < 2000:
                    score = 5
                else:
                    score = 2
    
                print(f"{place_type}: Mesafe {distance:.2f} m, Puan: {score}")
                seen_types[place_type] = True  # Bu türdeki yerin zaten listelendiğini belirt
    else:
        print("Nearby locations API call failed.")
        print(f"Yanıt içeriği: {overpass_response.text}")

else:
    print("Adres bulunamadı veya geçersiz. Lütfen adresi kontrol edin.")
