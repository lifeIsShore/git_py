import requests
from bs4 import BeautifulSoup
import csv
import logging

# Set up logging configuration
logging.basicConfig(
    filename=r"C:\Users\ahmty\Desktop\web_scraper.log",  # Log dosyasının adı
    level=logging.INFO,  # Log seviyesi
    format='%(asctime)s - %(levelname)s - %(message)s',  # Log formatı
)

# URL of the first page
url = "https://www.immowelt.de/classified-search?distributionTypes=Buy,Buy_Auction,Compulsory_Auction&estateTypes=House&locations=AD08DE5960&page=1&order=DateDesc"  
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Find the pagination list containing page numbers
pagination = soup.find("ul", class_="css-bcim1s")  # The <ul> class that contains page numbers

# Add page numbers to a list
page_numbers = []
if pagination:
    for li in pagination.find_all("li"):
        button = li.find("button")
        if button:
            page_num = button.text.strip()
            # Convert page number to an integer
            if page_num.isdigit():  # Check if the page number is a digit
                page_numbers.append(int(page_num))

# Find the last page number
last_page_num = max(page_numbers) if page_numbers else 1  # Set to 1 if page_numbers is empty
logging.info(f"Last page number: {last_page_num}")  # Log the last page number

# Variables for tracking the scraping progress
total_records = 0
unknown_count = 0
unknown_rows = []

# Create and write to the CSV file
with open(r"C:\Users\ahmty\Desktop\ads.csv", mode='w', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file)
    # Write the header row to the CSV file
    writer.writerow(["Street", "City_Code", "Price", "Number of Rooms", "Living Area", "Land Size"])

    # Retrieve data from all pages
    for page in range(1, last_page_num + 1):
        logging.info(f"Scraping page {page}...")  # Log the page number being scraped
        response = requests.get(f"https://www.immowelt.de/classified-search?distributionTypes=Buy,Buy_Auction,Compulsory_Auction&estateTypes=House&locations=AD08DE5960&page={page}&order=DateDesc")
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract listings from each page
        listings = soup.find_all("div", class_="css-gg38ii")  # The <div> that contains each listing

        for idx, listing in enumerate(listings, start=1):  # Include the index (starting from 1) to track row number
            address = listing.find("div", class_="css-ee7g92").text.strip()  # Extract the address from the listing
            price = listing.find("div", class_="css-11nox3k").text.strip()  # Extract the price class
            features = listing.find_all("div", class_="css-9u48bm")  # Extract features for this listing
            
            # Extract number of rooms, living area, and land size
            rooms = features[0].text.strip() if len(features) > 0 else "Unknown"  # First feature (rooms)
            living_area = features[2].text.strip() if len(features) > 2 else "Unknown"  # Third feature (living area)
            land_size = features[4].text.strip() if len(features) > 4 else "Unknown"  # Fifth feature (land size)

            # Track unknown values
            unknowns = []
            if rooms == "Unknown":
                unknowns.append("rooms")
            if living_area == "Unknown":
                unknowns.append("living_area")
            if land_size == "Unknown":
                unknowns.append("land_size")
            
            if unknowns:
                unknown_count += 1
                unknown_rows.append((idx, unknowns))  # Add row index and unknown feature(s) to the list

            # Write the data to the CSV file
            writer.writerow([address, price, rooms, living_area, land_size])
            total_records += 1

        logging.info(f"Finished scraping page {page}.")  # Log when a page has been scraped

# Log the final counts
logging.info(f"Total records scraped: {total_records}")
logging.info(f"Total unknown values found: {unknown_count}")
for row in unknown_rows:
    logging.info(f"Row {row[0]} has unknown values: {', '.join(row[1])}")

logging.info("Data has been successfully saved to 'ads.csv'.")  # Log when all data is saved
