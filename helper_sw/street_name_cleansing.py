import pandas as pd
import re
import os

# Dosyanın bulunduğu yol
input_file_path = r"C:\Users\ahmty\Desktop\Python\geo_DSproject_github_clone\git_py\csv_output\combined\combined.csv"
# Temizlenmiş CSV dosyasının kaydedileceği yol
output_file_path = r"C:\Users\ahmty\Desktop\Python\geo_DSproject_github_clone\git_py\csv_output\combined\cleaned_output1.csv"

# Fiyatla ilgili olan kısımları temizlemek için fonksiyon
def clean_price(text):
    # Fiyatla ilgili olan kısmı silmek için regex kullanıyoruz
    # '¬', 'Â', 'â‚¬', '/m²', vb. karakterleri temizle
    text = re.sub(r'Â|\s?â‚¬|\s?/m²|\s?¬', '', text)
    return text

# CSV dosyasını oku
df = pd.read_csv(input_file_path, encoding='windows-1252')

# Fiyat ve diğer kolonlarda temizleme işlemi yapıyoruz
for column in df.columns:
    df[column] = df[column].apply(lambda x: clean_price(str(x)))

# Temizlenmiş veriyi yeni bir dosyaya kaydediyoruz
df.to_csv(output_file_path, index=False, encoding='windows-1252')

print(f"Dosya başarıyla temizlendi ve kaydedildi: {output_file_path}")


