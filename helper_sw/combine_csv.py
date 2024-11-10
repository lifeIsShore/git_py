import pandas as pd
import glob
import os

# Dosyaların bulunduğu klasörün yolu
input_folder_path = r"C:\Users\ahmty\Desktop\Python\geo_DSproject_github_clone\git_py\csv_output\web_scraping\web_scraping_ID"
# Birleştirilmiş CSV dosyasının kaydedileceği klasör
output_folder_path = r"C:\Users\ahmty\Desktop\Python\geo_DSproject_github_clone\git_py\csv_output\combined"

# Tüm CSV dosyalarının yolunu al
csv_files = glob.glob(os.path.join(input_folder_path, "*.csv"))

# CSV dosyalarını tek bir DataFrame'de birleştir (hatalı satırları atla)
combined_df = pd.concat([pd.read_csv(file, on_bad_lines='skip', encoding='windows-1252', sep=';') for file in csv_files], ignore_index=True)

# Eğer bazı kolonlar hala yanlış ayrılmışsa, bunları düzeltmek için sonrasında manuel düzeltme yapılabilir.
# Örneğin, city_id'nin son sütun olduğuna eminseniz ve son sütun bozuksa onu doğru şekilde düzeltebilirsiniz.

# City ID gibi hatalı formatları düzeltme: örneğin, 'city_ID' doğru formatta olmalı.

# Birleştirilen DataFrame'i yeni klasöre kaydet (encoding 'windows-1252' ile)
output_path = os.path.join(output_folder_path, "combined_output3.csv")
combined_df.to_csv(output_path, index=False, encoding='windows-1252')

print("Dosyalar başarıyla birleştirildi ve kaydedildi:", output_path)
