import csv
from web_scrapper import scrape_immowelt  # İlk kodunuzun bulunduğu dosya adıyla değiştirin

# CSV dosyasındaki URL'leri okuma ve scrape_immowelt fonksiyonunu çağırma
def process_urls_from_csv(input_csv, output_dir):
    """
    Reads URLs from a CSV file and processes each URL using the scrape_immowelt function.

    Args:
        input_csv (str): Path to the input CSV file containing the list of URLs.
        output_dir (str): Directory path where the CSV and log files will be saved.
    """
    with open(input_csv, mode='r', newline='', encoding='utf-8-sig') as file:
        reader = csv.reader(file, delimiter=';')  # Delimiter olarak `;` belirtiyoruz
        next(reader, None)  # Optional: Skip the header row if your CSV has one
        for row in reader:
            url = row[-1]  # URL is assumed to be in the last column
            print(f"Processing URL: {url}")
            try:
                scrape_immowelt(url, output_dir)
                print(f"Completed scraping for URL: {url}")
            except Exception as e:
                print(f"Error processing URL {url}: {e}")

    # Print message when all URLs have been processed
    print("Finished processing all URLs.")

# CSV dosyasının konumu ve çıktı klasörünün yolu
input_csv = r"C:\Users\ahmty\Desktop\Python\geo_DSproject_github_clone\git_py\csv_input\immowelt_urls_copy (used in web scraping).csv"
output_dir = r"C:\Users\ahmty\Desktop\Python\geo_DSproject_github_clone\git_py\csv_output\web_scraping"

# URL'leri işleme
process_urls_from_csv(input_csv, output_dir)
