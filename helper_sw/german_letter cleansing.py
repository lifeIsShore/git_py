import pandas as pd
import re
import os

# Dosyanın bulunduğu yol
input_file_path = r"C:\Users\ahmty\Desktop\Python\geo_DSproject_github_clone\git_py\csv_output\combined\cleaned_output1.csv"
# Temizlenmiş CSV dosyasının kaydedileceği yol
output_file_path = r"C:\Users\ahmty\Desktop\Python\geo_DSproject_github_clone\git_py\csv_output\combined\cleaned_u-free.csv"

# Fiyatla ilgili olan kısımları temizlemek için fonksiyon
def clean_price(text):
    # Fiyatla ilgili olan kısmı silmek için regex kullanıyoruz
    # '¬', 'Â', 'â‚¬', '/m²', vb. karakterleri temizle
    text = re.sub(r'Â|\s?â‚¬|\s?/m²|\s?¬', '', text)
    return text

# Özel karakterleri düzeltmek için fonksiyon
def correct_special_characters(text):
    # 'Ã¼' yerine 'ü' düzeltmesi yapalım
    text = text.replace('Ã¼', 'u')  # 'Ã¼' karakteri 'ü' ile değiştirilecek
    return text

# CSV dosyasını oku
df = pd.read_csv(input_file_path, encoding='windows-1252')

# Tüm kolonlardaki her hücreyi temizliyoruz
for column in df.columns:
    # Önce fiyatla ilgili temizleme işlemi
    df[column] = df[column].apply(lambda x: clean_price(str(x)))
    # Ardından özel karakter düzeltme işlemi
    df[column] = df[column].apply(lambda x: correct_special_characters(str(x)))

# Temizlenmiş veriyi yeni bir dosyaya kaydediyoruz
df.to_csv(output_file_path, index=False, encoding='windows-1252')

print(f"Dosya başarıyla temizlendi ve kaydedildi: {output_file_path}")
