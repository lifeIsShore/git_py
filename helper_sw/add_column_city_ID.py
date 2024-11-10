import os
import pandas as pd
import re  # Regex modülünü ekliyoruz

# Yeni dosyaların bulunduğu klasör yolu
new_folder_path = r"C:\Users\ahmty\Desktop\Python\geo_DSproject_github_clone\git_py\csv_output\web_scraping\web_scraping_ID"

# 1. Yeni dosyaların bulunduğu klasördeki tüm CSV dosyalarını listeleme
files = [f for f in os.listdir(new_folder_path) if f.endswith('.csv')]

# 2. Her bir dosya için işlemleri gerçekleştirme
for file in files:
    file_path = os.path.join(new_folder_path, file)
    
    # Dosya adındaki sadece sayıyı almak (parantez içindeki sayıyı hariç tutmak için regex kullanıyoruz)
    match = re.match(r"(\d+)", os.path.splitext(file)[0])  # Dosya adındaki ilk sayıyı alıyoruz
    if match:
        city_id = match.group(1)  # İlk sayıyı city_id olarak alıyoruz
    else:
        city_id = os.path.splitext(file)[0]  # Eğer sayı bulunmazsa dosya adının tamamını kullanıyoruz
    
    # CSV dosyasını okuma
    df = pd.read_csv(file_path, delimiter=';')
    
    # Dosya adını (city_id) son sütun olarak ekleme
    df['city_id'] = city_id  # Yeni sütun olarak ekliyoruz
    
    # Güncellenmiş dosyayı aynı isimle kaydetme (veya yeni bir isimle kaydedebilirsiniz)
    df.to_csv(file_path, sep=';', index=False)
    
    print(f"{file} dosyasına city_id eklendi ve güncellendi.")

print("Tüm dosyalar başarıyla güncellendi.")
