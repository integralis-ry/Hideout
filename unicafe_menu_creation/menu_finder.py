from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
import time

def navigate_and_save(driver, restaurant_name):
    wait = WebDriverWait(driver, 30)
    restaurant_button = wait.until(EC.element_to_be_clickable((By.XPATH, f"//button[contains(text(), '{restaurant_name}')]")))
    restaurant_button.click()

    time.sleep(10)
    page_source = driver.page_source
    file_path = f'../unicafe_menu_creation/to_scrape_htmls/{restaurant_name.lower()}_page_source.html'

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(page_source)
    print(f"{restaurant_name} saved to {os.path.abspath(file_path)}")

if __name__ == "__main__":
    url = 'https://unicafe.fi/en'

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    service = Service(executable_path="/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(url)
    restaurants = ['Exactum', 'Chemicum', 'Physicum']

    for restaurant in restaurants:
        navigate_and_save(driver, restaurant)

    driver.quit()
    print("All restaurant pages have been saved.")