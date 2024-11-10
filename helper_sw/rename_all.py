import os
import pandas as pd
import shutil  # Dosya kopyalama için shutil modülünü ekliyoruz

# Dosya yolları
web_scraping_path = r"C:\Users\ahmty\Desktop\Python\geo_DSproject_github_clone\git_py\csv_output\web_scraping"
new_folder_path = r"C:\Users\ahmty\Desktop\Python\geo_DSproject_github_clone\git_py\csv_output\web_scraping\web_scraping_ID"
city_id_csv_path = r"C:\Users\ahmty\Desktop\immowelt_urls_copy (used in web scraping).csv"

# Yeni klasörün var olup olmadığını kontrol et ve yoksa oluştur
if not os.path.exists(new_folder_path):
    os.makedirs(new_folder_path)

# 1. City_ID'leri içeren CSV dosyasını okuma (noktalı virgül ayracı ile)
city_id_df = pd.read_csv(city_id_csv_path, delimiter=';')
city_id_df.columns = city_id_df.columns.str.strip().str.lower()  # Sütun adlarını temizleme ve küçük harfe çevirme

# city_id sütununun varlığını kontrol etme
if 'city_id' in city_id_df.columns:
    city_ids = city_id_df['city_id'].tolist()  # city_id değerlerini listeye çevirme
else:
    raise KeyError("Error: 'city_id' column not found in the CSV file.")

# 2. web_scraping klasöründeki dosyaları creation date'e göre sıralama
files = [f for f in os.listdir(web_scraping_path) if os.path.isfile(os.path.join(web_scraping_path, f))]
files.sort(key=lambda f: os.path.getctime(os.path.join(web_scraping_path, f)))

# 3. Dosya sayısı ve city_id sayısını kontrol etme
if len(files) != len(city_ids):
    print("Hata: Dosya sayısı ve city_id sayısı eşleşmiyor.")
else:
    # 4. Dosyaları yeni isimleri ile kopyalama ve yeni klasöre taşıma
    for file, city_id in zip(files, city_ids):
        old_file_path = os.path.join(web_scraping_path, file)
        new_file_name = f"{city_id}.csv"
        new_file_path = os.path.join(new_folder_path, new_file_name)

        # Aynı isimde dosya varsa, (1), (2), (3) gibi bir ek ekleyerek yeni ismi oluşturma
        counter = 1
        while os.path.exists(new_file_path):
            new_file_path = os.path.join(new_folder_path, f"{city_id} ({counter}).csv")
            counter += 1

        # Dosyayı kopyalayarak yeni klasöre kopyalama ve adını değiştirme
        shutil.copy(old_file_path, new_file_path)

    print("Dosyalar başarılı bir şekilde kopyalandı ve yeni klasöre adlandırıldı.")
