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
    
    btn = wait.until(EC.presence_of_element_located((By.XPATH, f"//button[contains(text(), '{restaurant_name}')]")))
    driver.execute_script("arguments[0].scrollIntoView();", btn)
    driver.execute_script("arguments[0].click();", btn)
    
    try:
        friday_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Fri')]")))
        driver.execute_script("arguments[0].click();", friday_btn)
        print(f"Switched to Friday tab for {restaurant_name}")
    except Exception as e:
        print(f"Could not find Friday tab for {restaurant_name}, staying on default.")

    time.sleep(10) 
    
    page_source = driver.page_source
    base_dir = "/home/integralis/Hideout/unicafe_menu_creation/to_scrape_htmls"
    os.makedirs(base_dir, exist_ok=True)
    file_path = os.path.join(base_dir, f"{restaurant_name.lower()}_page_source.html")

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(page_source)
    print(f"{restaurant_name} saved to {file_path}")

if __name__ == "__main__":
    url = 'https://unicafe.fi/en'

    options = Options()
    # options.add_argument("--headless") 
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--start-maximized")
    
    service = Service(executable_path="/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)

    # Set window size to ensure buttons are visible
    driver.set_window_size(1920, 1080)

    driver.get(url)
    
    # Optional: Wait for and click a "Reject/Accept Cookies" if it blocks the view
    try:
        cookie_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll")))
        cookie_btn.click()
    except:
        pass

    restaurants = ['Exactum', 'Chemicum', 'Physicum']

    for restaurant in restaurants:
        navigate_and_save(driver, restaurant)

    driver.quit()
    print("All restaurant pages have been saved.")
