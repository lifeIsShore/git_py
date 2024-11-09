1- URL of the first page: This line specifies the URL of the first page of the real estate listings that will be scraped.

2- Find the pagination list containing page numbers: This comment indicates that the code is looking for a specific HTML element (an unordered list) that contains the page numbers for pagination.

3- Add page numbers to a list: Here, the code iterates through each list item in the pagination to extract the page numbers.

4- Convert page number to an integer: This comment highlights the check to ensure that the text extracted is a valid digit before converting it to an integer.

5- Find the last page number: This comment explains how the last page number is determined from the list of page numbers. If no page numbers are found, it defaults to 1.

6- Create and write to the CSV file: This comment indicates the start of the process to create a new CSV file and prepare it for writing data.

7- Write the header row to the CSV file: This line specifies the column headers for the CSV file, providing a structure for the data that will be recorded.

8- Retrieve data from all pages: This comment explains that the following code will loop through all the pages to collect listings data.

9- Extract listings from each page: Here, the code retrieves all listings from the current page.

10- Extract the address from the listing: This comment explains that the code extracts the address information from the HTML structure of each listing.

11- Extract the price class: This comment notes that the code is pulling the price information from the corresponding HTML element.

12- Extract features for this listing: This comment indicates that various features related to the listing (like number of rooms and size) are being retrieved.

13- Extract number of rooms: This comment specifies that the code retrieves the number of rooms, with a fallback to "Unknown" if no data is available.

14- Extract living area: Similar to the previous comment, this line retrieves the living area information.

15- Extract land size: This comment indicates that the code attempts to retrieve the land size from the features list.

16- Check if features have 3rd and 4th indices: This comment emphasizes that the code checks for the existence of additional feature indices before attempting to access them.

17- Update land size from the 4th feature: This comment notes that if the 4th feature exists, it is used to update the land size.

18- Write the data to the CSV file: This comment indicates that the extracted data for the current listing is written into the CSV file.

19- Data has been successfully saved to 'ilanlar.csv': This final print statement confirms that the data scraping and saving process has completed successfully.