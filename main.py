from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import json
all_data = []
def scrape():
    # Initialize the driver
    driver = webdriver.Chrome()

    # Open the target URL
    driver.get("https://results.eci.gov.in/ResultAcGenNov2024/statewiseS131.htm")

    # Function to scrape table data
    def scrape_table():
        try:
            # Locate the table
            table = driver.find_element(By.XPATH, "/html/body/main/div/div[3]/div/table")
            rows = table.find_elements(By.TAG_NAME, "tr")

            # Extract headers
            headers = [header.text for header in rows[1].find_elements(By.TAG_NAME, "th")]

            # Extract data rows
            data = []
            for row in rows[1:]:  # Skip header row
                cells = row.find_elements(By.TAG_NAME, "td")
                row_data = [cell.text for cell in cells]
                data.append(row_data)

            return headers, data

        except NoSuchElementException:
            print("Error: Table not found on the page.")
            return None, None

    # Scrape data across multiple pages

    for page in range(1, 16):  # Loop through pages 1 to 15
        print(f"Scraping page {page}...")
        headers, data = scrape_table()
        if headers and data:
            all_data.append({
                "page": page,
                "headers": headers,
                "data": data
            })

        # Click the "Next" button to go to the next page
        try:
            next_button = driver.find_element(By.XPATH, f"/html/body/main/div/div[4]/div/div/ul/li[{page + 1}]/a")
            driver.execute_script("arguments[0].scrollIntoView();", next_button)
            driver.execute_script("arguments[0].click();", next_button)
            time.sleep(2) # Wait for the next page to load
        except NoSuchElementException:
            print("No more pages to navigate.")
            break

    # Close the driver
    driver.quit()

scrape()
# Print all scraped data
new_data = []
for page_data in all_data:
    print(f"Page {page_data['page']}:")
    print("Headers:", page_data['headers'])

    for row in page_data['data']:
        # Check if the row has at least 6 elements and the 6th element (index 5) contains 'i'
        if len(row) > 5 and 'i' in row[5]:
            # Add the filtered row to new_data
            new_data.append(row)
            print(row)

print("\nFiltered Data:")
for item in new_data:
    print(item)
with open("scraped_data.json", "w") as file:
    json.dump(new_data, file)
    print("Data saved to scraped_data.json")
