import requests
from bs4 import BeautifulSoup
import csv

# İlk sayfanın URL'si
url = "https://www.immowelt.de/classified-search?distributionTypes=Buy,Buy_Auction,Compulsory_Auction&estateTypes=House&locations=AD08DE5960&page=1&order=DateDesc"  
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Sayfa numaralarını içeren listeyi bulma
pagination = soup.find("ul", class_="css-bcim1s")  # Sayfa numaralarını içeren ul sınıfı

# Sayfa numaralarını listeye ekleme
page_numbers = []
if pagination:
    for li in pagination.find_all("li"):
        button = li.find("button")
        if button:
            page_num = button.text.strip()
            # Sayfa numarasını tam sayıya çevirme işlemi
            if page_num.isdigit():  # Eğer sayfa numarası bir rakam ise
                page_numbers.append(int(page_num))

# En son sayfa numarasını bulma
last_page_num = max(page_numbers) if page_numbers else 1  # Eğer page_numbers boşsa 1 olarak ayarla
print(f"En son sayfa numarası: {last_page_num}")

# CSV dosyasını oluşturma ve yazma işlemi
with open(r"C:\Users\ahmty\Desktop\ilanlar.csv", mode='w', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file)
    # CSV dosyasına başlık satırını yazma
    writer.writerow(["Adres", "Fiyat", "Oda Sayısı", "Yaşam Alanı", "Arsa Büyüklüğü"])

    # Tüm sayfalardan veri çekme
    for page in range(1, last_page_num + 1):
        response = requests.get(f"https://www.immowelt.de/classified-search?distributionTypes=Buy,Buy_Auction,Compulsory_Auction&estateTypes=House&locations=AD08DE5960&page={page}&order=DateDesc")
        soup = BeautifulSoup(response.text, "html.parser")

        # Her sayfadaki ilanları çekme işlemi
        listings = soup.find_all("div", class_="css-79elbk")  # Her ilanın div'i (gerçek sınıfı kontrol edin)

        for listing in listings:
            address = listing.find("div", class_="css-ee7g92").text.strip()  # Adresi listing içinden çek
            price = listing.find("div", class_="css-11nox3k").text.strip()  # Fiyat sınıfı
            features = listing.find_all("div", class_="css-9u48bm")  # Özellikler sadece bu listing için çekilsin
            
            rooms = features[0].text.strip() if len(features) > 0 else "Bilinmiyor"
            living_area = features[1].text.strip() if len(features) > 1 else "Bilinmiyor"
            land_size = features[2].text.strip() if len(features) > 2 else "Bilinmiyor"
            # Eğer features 3 ve 4. indekslere sahipse, onları kontrol et
            if len(features) > 3:
                land_size = features[3].text.strip()
            if len(features) > 4:
                land_size = features[4].text.strip()
            
            # CSV dosyasına verileri yazma
            writer.writerow([address, price, rooms, living_area, land_size])

print("Veriler başarıyla 'ilanlar.csv' dosyasına kaydedildi.")
