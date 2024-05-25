# Import necessary libraries
from selenium import webdriver
from selenium.webdriver.support.ui import Select

from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time


data = []

# Set up the initial parameters
startTime = time.time()
url = "https://web.splus.ir/#-100959274"

driver = webdriver.Chrome()  # Initialize the Chrome web driver


def login():
        driver.find_element(By.XPATH, value="//div[@class='DropdownMenu CountryCodeInput']").click()
        time.sleep(3)  # Pause for 3 second
        driver.find_element(By.XPATH, value="//span[@class='country-name' and contains(text(), 'Iran')]").click()
        phone_num = input("What is your phone number?(without 0 and Press enter at the end to continue):")
        driver.find_element(By.XPATH, value="//input[@id='sign-in-phone-number']").send_keys(phone_num)
        driver.find_element(By.XPATH, value="//button[@class='Button default primary has-ripple']").click()
        phone_code = input("Send SMS contain login code, Enter it?(Press enter at the end to continue):")
        driver.find_element(By.XPATH, value="//input[@id='sign-in-code']").send_keys(phone_code)
        time.sleep(8)

        driver.find_element(By.XPATH, value="//input[@id='search-input']").send_keys('ostad_shojae')
        time.sleep(5)
        driver.find_element(By.XPATH, value="//div[@class='search-section']/div[1]/div[1]/div[1]").click()
        try:
            driver.find_element(By.XPATH, value="//button[@class='Button tiny primary fluid has-ripple']").click()
        except:
            pass


driver.get(url)  # Open the specified URL
if driver.current_url != url:
    login()
actions = ActionChains(driver)

# Click on the element after waiting for it to be clickable
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "Transition"))).click()

# Scroll the page and gather data
for _ in range(5):
    # Scroll to the element
    driver.execute_script("arguments[0].scrollIntoView()",
                          driver.find_element(By.XPATH, value="//div[@class='sticky-date']"))
    # Simulate pressing the PAGE UP key
    actions.send_keys(Keys.PAGE_UP).perform()
    time.sleep(2)  # Pause for 2 second

items = driver.find_elements(By.XPATH, value="//div[@class='message-date-group']")
try:
    # Extract data from each message element
    for item in items:
        # Get the message Link or use '' if not found
        messages = item.find_elements(By.XPATH, value=".//div[contains(@id,'message')]")
        for message in messages:
            messageLink = message.find_element(By.XPATH, value=".//div[1]").get_attribute('data-message-id')\
                if message.find_elements(By.XPATH, value=".//div[1]") \
                else ""
            Link = "https://splus.ir/ostad_shojae/" + messageLink
            # Get the message view count or use '-1' if not found
            View = message.find_element(By.XPATH, value=".//span[@class='message-views']").text \
                if message.find_elements(By.XPATH, value=".//span[@class='message-views']") else "-1"
            if View != -1 and Link != "https://splus.ir/ostad_shojae/":
                data.append([Link, View])
except:
    pass


# Create a DataFrame and save it to a CSV file
df = pd.DataFrame(data, columns=['Link', 'View'])
df.to_csv("Splus.csv")

# Display the DataFrame and execution time
print(df)
print(f"How long does it take? {time.time() - startTime} seconds")
# select by visible text

while True:
    pass