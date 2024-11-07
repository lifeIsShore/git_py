import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import threading

# find the path
input_csv = r"C:\Users\ahmty\Desktop\project sources\germany_cities_zipcodes2.csv"
output_csv = r"C:\Users\ahmty\Desktop\project sources\immowelt_urls.csv"

# read from csv
zip_codes = pd.read_csv(input_csv)['ZipCode'].tolist()

# write a headline for the .csv (dynamic)
with open(output_csv, 'w', newline='', encoding='utf-8') as file:
    file.write("ZipCode,URL\n")

# Web scraping function
def scrape_zip_code(zip_code):
    try:
        # start WebDriver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

        # go to the Web
        driver.get("https://www.immowelt.de/")

        # find input elemetn and type zip
        input_field = driver.find_element(By.CSS_SELECTOR, "input[aria-label='Ort oder Postleitzahl eingeben']")
        input_field.clear()  # clean last value
        input_field.send_keys(zip_code)

        # wait before click enter
        time.sleep(2)  # 2 seconds before action 
        input_field.send_keys(Keys.RETURN)  # click enter

        # wait for the page reload
        time.sleep(3)  # ... second wait

        # take new url
        current_url = driver.current_url
        # URL cleansing (trim after &order) 
        clean_url = current_url.split("&order")[0]

        # save URLs to .csv
        with open(output_csv, 'a', newline='', encoding='utf-8') as file:
            file.write(f"{zip_code},{clean_url}\n")

        print(f"ZIP code {zip_code}, URL is saved: {clean_url}")

        driver.quit()

    except Exception as e:
        print(f"Error occured for {zip_code} zip code: {e}")

# list for Thread
threads = []
max_threads = 10  # max thread that work at the same time

# create parallel threads
for i in range(0, len(zip_codes), max_threads):
    current_batch = zip_codes[i:i+max_threads]  # every batch 10 ZIP code
    for zip_code in current_batch:
        thread = threading.Thread(target=scrape_zip_code, args=(zip_code,))
        threads.append(thread)
        thread.start()

    # Batch'in tamamlanmasını bekle
    for thread in threads[-len(current_batch):]:
        thread.join()

print("Scraping is done.")
