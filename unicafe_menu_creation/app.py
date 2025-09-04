from flask import Flask, render_template
from bs4 import BeautifulSoup
import logging
import os
from datetime import datetime
# use curl to get htmls instead of firefox
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
import time


app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def parse_menu_items(soup):
    menu_items = []
    food_items = soup.find_all('div', class_='l-restaurants__menus__item__grid__item')
        
    if not food_items:
        logging.warning("No food items found in the HTML")
        return menu_items

    for item in food_items:
        title = item.find('h3', class_='l-restaurants__menus__item__grid__item__title')
        if not title:
            logging.warning("Food item found but no title available")
            continue
        
        title = title.text.strip()
        category = item.find('span', class_='l-restaurants__menus__item__grid__item__tag')
        category = category.text.strip() if category else "Unknown Category"
        
        icons = item.find('div', class_='l-restaurants__menus__item__grid__item__icons')
        diets = [img['alt'] for img in icons.find_all('img')] if icons else []
        
        allergens = item.find('p',
                              class_='l-restaurants__menus__item__grid__item__subcontent--allergens')
        allergens = allergens.text.strip() if allergens else ""
        
        menu_items.append({
            'title': title,
            'category': category,
            'diets': ', '.join(diets),
            'allergens': allergens
        })
    
    logging.info(f"Found {len(menu_items)} menu items")
    return menu_items

def get_physicum_menu():
    return [
        {
            'title': 'Panini',
            'category': 'Lunch',
            'diets': '',
            'allergens': ''
        },
        {
            'title': 'Salad',
            'category': 'Lunch',
            'diets': '',
            'allergens': ''
        },
        {
            'title': 'Baguette sandwich',
            'category': 'Lunch',
            'diets': '',
            'allergens': ''
        }
    ]

def get_menu_data():
    menu_data = {}
    restaurants = ['exactum', 'chemicum', 'physicum']

    for restaurant in restaurants:
        if restaurant == 'physicum':
            menu_data[restaurant] = get_physicum_menu()
            continue

        filename = f"../unicafe_menu_creation/to_scrape_htmls/{restaurant}_page_source.html"
        if not os.path.exists(filename):
            logging.warning(f"File not found: {filename}")
            continue

        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()

        soup = BeautifulSoup(content, 'html.parser')
        menu_data[restaurant] = parse_menu_items(soup)
        if menu_data[restaurant]:
            menu_data[restaurant].pop()

    if not menu_data:
        logging.error("No menu data found in any of the files")

    return menu_data

def save_rendered_html(html_content):
    file_path = "../display/unicafe_menu.html"
    default_filename = "menu_data.html"
    
    try:
        #write the date file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(html_content)
        logging.info(f"Saved rendered HTML to {file_path}")

        # Write to default file
        with open(default_filename, 'w', encoding='utf-8') as file:
            file.write(html_content)
        logging.info(f"Also saved rendered HTML to {default_filename}")

    except Exception as e:
        logging.error(f"Error saving rendered HTML: {str(e)}")

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

    # Get the page sourcemenu_data_20241101
    page_source = driver.page_source

    # Define the file path
    file_path = f'../unicafe_menu_creation/to_scrape_htmls/{restaurant_name.lower()}_page_source.html'

    # Write the page source to a file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(page_source)

    print(f"{restaurant_name} page source has been saved to {os.path.abspath(file_path)}")



@app.route('/')
def index():

    filename = f'menu_data_{datetime.now().strftime("%Y%m%d")}.html'
    
    if not os.path.exists(filename):
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

    menu_data = get_menu_data()

    if not menu_data:
        logging.error("No menu data available to display")
        return "Error: Unable to fetch menu data", 500
        
    rendered_html = render_template('index.html', menu_data=menu_data)

    save_rendered_html(rendered_html)

    return rendered_html

def get_rendered_html():
    with app.test_client() as client:
        response = client.get('/')
        return response.data.decode('utf-8')

if __name__ == '__main__':
    # Instead of running the server, just get and save the rendered HTML
    timestamp = datetime.now().strftime("%Y%m%d")
    filename = f"menu_data_{timestamp}.html"
    
    if filename in os.listdir():
        logging.info(f"File {filename} already exists. Skipping rendering.")
    else:
        for old_file in os.listdir():
            if old_file.startswith("menu_data_"):
                os.remove(old_file)
                logging.info(f"Removed old file: {old_file}")
        # use menu_data saving for render
        # make sure to close the webscraper in case of errors
        html_content = get_rendered_html()
        save_rendered_html(html_content)