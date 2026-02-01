from flask import Flask, render_template
from bs4 import BeautifulSoup
import logging
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

app = Flask(__name__)
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
    wait = WebDriverWait(driver, 30)
    try:
        restaurant_button = wait.until(EC.presence_of_element_located(
            (By.XPATH, f"//button[contains(text(), '{restaurant_name}')]")
        ))
        
        driver.execute_script("arguments[0].click();", restaurant_button)

        time.sleep(5)
        
        page_source = driver.page_source
        file_path = f'../unicafe_menu_creation/to_scrape_htmls/{restaurant_name.lower()}_page_source.html'
        
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(page_source)
            
    except Exception as e:
        logging.error(f"Failed to scrape {restaurant_name}: {str(e)}")

@app.route('/')
def index():
    filename = f'menu_data_{datetime.now().strftime("%Y%m%d")}.html'
    
    if not os.path.exists(filename):
        url = 'https://unicafe.fi/en'

        # Chromium Setup
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        service = Service(executable_path="/usr/bin/chromedriver")
        driver = webdriver.Chrome(service=service, options=options)

        driver.get(url)
        for restaurant in ['Exactum', 'Chemicum', 'Physicum']:
            navigate_and_save(driver, restaurant)
        driver.quit()

    menu_data = get_menu_data()
    if not menu_data:
        return "Error: Unable to fetch menu data", 500
        
    rendered_html = render_template('index.html', menu_data=menu_data)
    save_rendered_html(rendered_html)
    return rendered_html

def get_rendered_html():
    with app.test_client() as client:
        response = client.get('/')
        return response.data.decode('utf-8')

if __name__ == '__main__':
    MENU_DIR = "/home/integralis/Hideout/unicafe_menu_creation"
    
    # always clear old HTML scraps to ensure a fresh parse
    scrape_dir = os.path.join(MENU_DIR, "to_scrape_htmls")
    if os.path.exists(scrape_dir):
        for f in os.listdir(scrape_dir):
            if f.endswith(".html"):
                os.remove(os.path.join(scrape_dir, f))

    html_content = get_rendered_html()
    save_rendered_html(html_content)
    logging.info("Menu successfully refreshed.")
