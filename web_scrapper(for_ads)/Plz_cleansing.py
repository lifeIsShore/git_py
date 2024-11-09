import pandas as pd
import json
import re

# JSON dosyasını oku
json_file_path = r"C:\Users\ahmty\Downloads\georef-germany-postleitzahl (2).json"  # JSON dosyasının yolu
csv_file_path = r"C:\Users\ahmty\Desktop\output_plz_names.csv"  # Çıktı CSV dosyasının yolu

# JSON dosyasını yükle
with open(json_file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# "plz_name_long" değerlerini al ve düzenle
plz_names_long = []
for item in data:
    if 'plz_name_long' in item:
        # Aralarında boşluk bulunmayan sayıyı ve ardından gelen ilk kelimeyi al
        match = re.search(r'(\d+)\s*(\w+)', item['plz_name_long'])
        if match:
            plz_names_long.append(f"{match.group(1)} {match.group(2)}")

# DataFrame oluştur
df = pd.DataFrame(plz_names_long, columns=['plz_name_long'])

# DataFrame'i CSV dosyasına yaz (UTF-8-SIG kodlaması ile)
df.to_csv(csv_file_path, index=False, encoding='utf-8-sig')

print("CSV dosyası başarıyla oluşturuldu:", csv_file_path)
