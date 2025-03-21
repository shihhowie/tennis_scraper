from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime,timedelta
import sys
import time

from sql_util import write_to_db
import chromedriver_autoinstaller

chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--no-sandbox")  # Required for EC2
chrome_options.add_argument("--disable-dev-shm-usage")  # Required for EC2
chrome_options.add_argument("--disable-gpu")  # Disable GPU for headless mode
chrome_options.add_argument("--window-size=1920x1080")  # Set window size
chrome_options.binary_location='/opt/chrome/chrome-linux64/chrome'
CHROMEDRIVER_PATH = "/opt/bin/chromedriver"  # Update this path if needed

# driver_path=chromedriver_autoinstaller.install()  # Automatically downloads and installs the matching Chromedriver
# Initialize the WebDriver
def query_tennis_court(court_name, base_url):
    # driver_path = chrome_aws_lambda.chromedriver_path if chrome_aws_lambda else None
    service = Service(executable_path="/opt/chrome-driver/chromedriver-linux64/chromedriver",
                      servicelog_path="/tmp/chromedriver.log") 
    driver = webdriver.Chrome(service=service, options=chrome_options)

    today = datetime.now().date()
    write_time = int(time.time())
    for i in range(7):
        date = today+timedelta(days=i)
        datestring = date.strftime('%Y-%m-%d')
        print(datestring)
        datestring_db = date.strftime('%Y%m%d')
        try:
            # Navigate to the booking page
            url = f'{base_url}/{datestring}/by-time'
            print(url)
            driver.get(url)

            # Wait for the booking slots to load
            wait = WebDriverWait(driver, 10)
            parent_divs = wait.until(EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, '.ClassCardComponent__Row-sc-1v7d176-1.vexzn')
            ))

            # Loop through each parent div and parse child elements
            for parent in parent_divs:
                # Get class time (child element)
                class_time = parent.find_element(By.CSS_SELECTOR, '.ClassCardComponent__ClassTime-sc-1v7d176-3.ePikrL').text
                space = 0
                # Get booking information (child element)
                try:
                    booking_info = parent.find_element(By.CSS_SELECTOR, '.ContextualComponent__BookWrap-sc-eu3gk6-1.dONMwG').text
                    space = int(booking_info.split(" ")[0])
                except Exception:
                    booking_info = "Booking information not available"
            

                if space > 0:
                # Print the parsed information
                    print(f"Class Time: {class_time}")
                    start_time, end_time = class_time.split("-")
                    start_time = datetime.strptime(start_time.strip(), "%H:%M").hour
                    end_time = datetime.strptime(end_time.strip(), "%H:%M").hour
                    print(f"Booking Info: {booking_info}")
                    num_slots = booking_info[0]
                    print("-" * 40)
                    #print(datestring_db, start_time, end_time, num_slots)
                    sql = f"""
                        INSERT INTO tennis_court_schedule (name, req_time, req_date, start_time, end_time, num_slots)
                        VALUES('{court_name}', {write_time}, {datestring_db}, {start_time}, {end_time}, {num_slots});
                    """
                    write_to_db(sql)
        except Exception as e:
            print(f'An error occurred: {e}')
        time.sleep(1)

    driver.quit()

def lambda_handler(event, context):
    query_tennis_court("islington_tennis_centre", "https://bookings.better.org.uk/location/islington-tennis-centre/tennis-court-indoor")
    query_tennis_court("rosemary_garden_tennis", "https://bookings.better.org.uk/location/islington-tennis-centre/rosemary-gardens-tennis")
    return {"statusCode": 200, "body": "Scraping completed successfully"}

if __name__ == '__main__':
    query_tennis_court("islington_tennis_centre", "https://bookings.better.org.uk/location/islington-tennis-centre/tennis-court-indoor")
    query_tennis_court("rosemary_garden_tennis", "https://bookings.better.org.uk/location/islington-tennis-centre/rosemary-gardens-tennis")
