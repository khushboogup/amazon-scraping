from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import pandas as pd

chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

df = pd.read_csv('paginationlinks.csv')
data_list1 = []
total_links = len(df['amazonlinks'])  

# Counter for link position
for link_no, link in enumerate(df['amazonlinks'], start=1):
    try:
        full_links = f"https://www.amazon.in/s?k=laptop{link}"
        
        # Added: Print current link number
        print(f"\nProcessing link {link_no}/{total_links}: {full_links}")
        
        driver.get(full_links)
        
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".s-result-item"))
        )
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        products = soup.find_all('div', {'data-component-type': 's-search-result'})

        product_count = 0
        
        for product in products:
            product_data = {}
            
            name_tag = product.find('h2', class_='a-size-medium')
            product_data['name'] = name_tag.text.strip() if name_tag else 'N/A'
            
            rating_tag = product.find('span', class_='a-icon-alt')
            product_data['rating'] = rating_tag.text.split()[0] if rating_tag else 'N/A'
            
            price_tag = product.find('span', class_='a-price-whole')
            product_data['price'] = price_tag.text.replace(',', '') if price_tag else 'N/A'
            
            link_tag = product.find('a', class_='a-link-normal')
            product_data['link'] = f"https://www.amazon.in{link_tag['href']}" if link_tag else 'N/A'
            
            
            data_list1.append(product_data)
            product_count += 1
            df=pd.DataFrame(data_list1,columns=['name','rating','price','link'])
            print(df)
            df.to_csv('Product.csv',index=False)
            
        # Added: Print results for this page
        print(f"Found {product_count} products on this page")

    except Exception as e:
        print(f"\n Error processing link {link_no} ({full_links}): {str(e)}")
        # Fix: Changed 'options' to 'chrome_options'
        driver.quit()
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
    time.sleep(2)

driver.quit()
print("\nScraping completed!")