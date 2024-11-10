import pandas as pd
import os

# Dosyanın bulunduğu yol
input_file_path = r"C:\Users\ahmty\Desktop\Python\geo_DSproject_github_clone\git_py\csv_output\combined\cleaned_u-free_v1,columns.csv"
# Temizlenmiş dosyanın kaydedileceği yol
output_folder_path = r"C:\Users\ahmty\Desktop\Python\geo_DSproject_github_clone\git_py\csv_output\combined"

# CSV dosyasını oku
df = pd.read_csv(input_file_path, encoding='windows-1252', sep=";")

# Dosyayı okuduktan sonra ilk birkaç satırı kontrol edelim
print("Orijinal Veri (İlk 5 Satır):")
print(df.head())

# Her satırdaki işlem yapılacak fonksiyon
def process_row(row):
    # Satırdaki tüm elemanları listeye dönüştür
    row_elements = row.tolist()

    # Satırdaki hücre sayısını kontrol et
    num_cells = len(row_elements)
    print(f"Satırdaki hücre sayısı: {num_cells}")

    # Eğer satırda 8 veya daha fazla öğe varsa işlem yapalım
    if num_cells >= 8:
        # İlk elemanı al
        first_element = row_elements[0]

        # En son 7 elemanı al (sondan başlayarak)
        last_seven = row_elements[-7:]

        # İlk eleman ve son 7 elemanı birleştir
        processed_row = [first_element] + last_seven
        return processed_row
    else:
        # Eğer satırda 8 öğeden az varsa olduğu gibi döndür
        return row_elements

# Her satırı işle
processed_rows = df.apply(process_row, axis=1)

# Yeni DataFrame oluştur
processed_df = pd.DataFrame(processed_rows.tolist(), columns=df.columns[:8])  # İlk 8 kolon ismini alıyoruz

# Temizlenmiş veriyi yeni bir dosyaya kaydet
output_file_path = os.path.join(output_folder_path, "cleaned_u-free_v1_processed.csv")
processed_df.to_csv(output_file_path, index=False, encoding='windows-1252')

print(f"Dosya başarıyla işlenip kaydedildi: {output_file_path}")
