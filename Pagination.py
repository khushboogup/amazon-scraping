# libraries for selenium webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

# driver setup
chrome_options = Options()
chrome_options.add_argument("--start-maximized")  
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--disable-gpu")  
chrome_options.add_argument("--no-sandbox")  
service = Service(ChromeDriverManager().install())
driver= webdriver.Chrome(service=service, options=chrome_options)

driver.get("https://www.amazon.in/s?k=laptop")
time.sleep(5)
all_pagination_links=[]
while True:
    paginations_links=driver.find_elements(By.XPATH,'//a[contains(@class,"s-pagination-item")]')
    for link in paginations_links:
        data=link.get_attribute('href')
        if data and data not in all_pagination_links:
            all_pagination_links.append([data])
            print(all_pagination_links)
    try:
        next_button=WebDriverWait(driver,10).until(
            EC.element_to_be_clickable((By.XPATH,'//a[contains(@class,"s-pagination-next") and not(contains(@class,"s-pagination-disabled"))]'))
        )
        next_button.click()
        WebDriverWait(driver,10).until(EC.staleness_of(next_button))
        time.sleep(2)
    except:
       print("no more page")
       break
print(all_pagination_links)

flattened_links = [link[0] for link in all_pagination_links]
base_url='https://www.amazon.in/s?k=laptop'
process=[link.split(base_url)[1] for link in flattened_links if base_url in link]


df=pd.DataFrame(process,columns=['amazonlinks'])
df.to_csv('paginationlinks.csv',index=False)

