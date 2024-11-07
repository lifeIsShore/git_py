import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Zip kodlarının bulunduğu CSV dosyasının yolu
input_csv = r"C:\Users\ahmty\Desktop\project sources\germany_cities_zipcodes2.csv"
output_csv = r"C:\Users\ahmty\Desktop\project sources\immowelt_urls.csv"

# WebDriver'ı başlat
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# CSV dosyasından zip kodlarını oku
zip_codes = pd.read_csv(input_csv)['ZipCode'].tolist()

# Yeni CSV dosyasına başlık yaz
with open(output_csv, 'w', newline='', encoding='utf-8') as file:
    file.write("ZipCode,URL\n")

# Her zip kodu için işlemi başlat
for zip_code in zip_codes:
    try:
        # Web sitesini kapatıp tekrar aç
        driver.quit()
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))  # Yeni bir driver başlat

        # Web sitesine git
        driver.get("https://www.immowelt.de/")

        # ZIP kodu input elementini bul ve ZIP kodunu gir
        input_field = driver.find_element(By.CSS_SELECTOR, "input[aria-label='Ort oder Postleitzahl eingeben']")
        input_field.clear()  # Önceden girilen değerleri temizle
        input_field.send_keys(zip_code)

        # Enter'a basmadan önce birkaç saniye bekle
        time.sleep(2)  # 2 saniye bekle, gerekirse artırabilirsiniz
        input_field.send_keys(Keys.RETURN)  # Enter'a bas

        # Sayfanın yüklenmesi için bekle
        time.sleep(3)  # Sayfanın tam olarak yüklenmesini sağlamak için

        # Yeni URL'yi al
        current_url = driver.current_url
        # URL'yi istenen şekilde düzenle (parametre kısmını kaldır)
        clean_url = current_url.split("&order")[0]

        # URL'yi ve ZIP kodunu yeni CSV dosyasına kaydet
        with open(output_csv, 'a', newline='', encoding='utf-8') as file:
            file.write(f"{zip_code},{clean_url}\n")

        print(f"ZIP kodu {zip_code} için URL kaydedildi: {clean_url}")

    except Exception as e:
        print(f"ZIP kodu {zip_code} için hata oluştu: {e}")

# Tarayıcıyı kapat
driver.quit()

#need to run at least 4 loop at the same time