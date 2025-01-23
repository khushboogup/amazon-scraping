from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Setup ChromeDriver
chrome_options = Options()
chrome_options.add_argument("--start-maximized")  # Open browser in full screen
# chrome_options.add_argument("--headless")  # Run in headless mode (optional)
chrome_options.add_argument("--disable-gpu")  # Disable GPU for headless mode
chrome_options.add_argument("--no-sandbox")  # Sandbox mode for Linux
service = Service(ChromeDriverManager().install())

driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get("https://www.amazon.in/s?k=laptop")  # Replace with your target URL
time.sleep(5)  # Allow initial content to load

def click_next_button(driver):
  links = []
  try:
    while True:
      # Wait for the next button to be clickable
      next_button = WebDriverWait(driver, 10).until(
          EC.element_to_be_clickable((By.XPATH, '//a[contains(@class, "s-pagination-item") and contains(@class, "s-pagination-next") and contains(@class, "s-pagination-button") and contains(@class, "s-pagination-button-accessibility")]'))
      )

      # Click the next button
      next_button.click()

      # Wait for the page to load
      WebDriverWait(driver, 10).until(
          EC.presence_of_element_located((By.XPATH, '//a[contains(@class,"s-pagination-item") and contains(@class,"s-pagination-next") and contains(@class,"s-pagination-button") and contains(@class,"s-pagination-button-accessibility") and contains(@class,"s-pagination-separator")]'))
      )

      # Get all links on the current page (you can adjust the selector as needed)
      all_links = driver.find_elements(By.TAG_NAME, 's-pagination-item s-pagination-button s-pagination-button-accessibility')
      for link in all_links:
        # Extract and print the href attribute of each link
        href = link.get_dom_attribute('href')
        print(href)
        

  except Exception as e:
    print(f"An error occurred: {e}")
    # If a stale element reference error occurs, try again
    if "stale element reference" in str(e):
      print("Stale element reference encountered. Retrying...")
      click_next_button(driver)  # Retry clicking the next button

  return links

# Call the function
links = click_next_button(driver)
print(links)

