import pandas as pd

# Input dosyasının yolu
input_csv_path = r"C:\Users\ahmty\Desktop\Python\geo_DSproject_github_clone\git_py\csv_output\combined\will be used\data with geospatial\3_ready_for_cal_data.csv"

# CSV dosyasını oku
df = pd.read_csv(input_csv_path)

# Price_cleaned sütunundaki Q1 (25. persentil) ve Q3 (75. persentil) hesaplanır
Q1 = df['Price_cleaned'].quantile(0.25)
Q3 = df['Price_cleaned'].quantile(0.75)

# IQR (Interquartile Range) hesaplanır
IQR = Q3 - Q1

# Alt ve üst sınırlar belirlenir
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# IQR dışındaki veriler temizlenir
df_filtered = df[(df['Price_cleaned'] >= lower_bound) & (df['Price_cleaned'] <= upper_bound)]

# Temizlenmiş veriyi yeni dosyaya kaydet
output_csv_path = r"C:\Users\ahmty\Desktop\Python\geo_DSproject_github_clone\git_py\csv_output\combined\will be used\data with geospatial\4_filtered_data_without_outliers.csv"
df_filtered.to_csv(output_csv_path, index=False)

print(f"Outliers temizlendi ve veri şu dosyaya kaydedildi: {output_csv_path}")
