from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
import time

def navigate_and_save(driver, restaurant_name):
    # Wait for the button to be clickable and click it
    wait = WebDriverWait(driver, 30)
    restaurant_button = wait.until(EC.element_to_be_clickable((By.XPATH, f"//button[contains(text(), '{restaurant_name}')]")))
    restaurant_button.click()

    # Wait for the page to update
    time.sleep(5)

    # Get the current URL
    current_url = driver.current_url
    print(f"Current URL after clicking {restaurant_name}: {current_url}")

    # Get the page source
    page_source = driver.page_source

    # Define the file path
    file_path = f'to_scrape_htmls/{restaurant_name.lower()}_page_source.html'

    # Write the page source to a file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(page_source)

    print(f"{restaurant_name} page source has been saved to {os.path.abspath(file_path)}")

if __name__ == "__main__":
    url = 'https://unicafe.fi/en'

    # set up Firefox WebDriver using GeckoDriverManager
    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))

    # Open the main page
    driver.get(url)

    # List of restaurants
    restaurants = ['Exactum', 'Chemicum', 'Physicum']

    # Navigate to each restaurant page and save the HTML
    for restaurant in restaurants:
        navigate_and_save(driver, restaurant)

    # Close the browser
    driver.quit()

    print("All restaurant pages have been saved.")