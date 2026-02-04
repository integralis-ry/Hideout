import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import os

def get_wotd():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    service = Service(executable_path="/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)
    
    url = "https://www.finnishpod101.com/finnish-phrases/"
    
    try:
        driver.get(url)
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        word = soup.find(class_='wotd-item-word').get_text(strip=True)
        meaning = soup.find(class_='wotd-item-meaning').get_text(strip=True)

        example_items = soup.find_all(class_='wotd-example-item')
        examples_html = ""

        # DYNAMIC FOR LOOP: Iterates through whatever number of examples found
        for item in example_items:
            fi = item.find(class_='wotd-example-sentence').get_text(strip=True)
            en = item.find(class_='wotd-example-meaning').get_text(strip=True)
            
            # Append a formatted block for each example
            examples_html += f"""
            <div class="example-item">
                <span class="fi-text">{fi}</span>
                <span class="en-text">{en}</span>
            </div>
            """
            
        return {'word': word, 'meaning': meaning, 'examples_html': examples_html}
    finally:
        driver.quit()

def render_display(data):
    if not data: return
    
    with open('word_template.html', 'r', encoding='utf-8') as f:
        template = f.read()

    final_html = template.replace('{{WORD}}', data['word'])
    final_html = final_html.replace('{{MEANING}}', data['meaning'])
    final_html = final_html.replace('{{EXAMPLES}}', data['examples_html'])

    with open('word_configured.html', 'w', encoding='utf-8') as f:
        f.write(final_html)

if __name__ == "__main__":
    data = get_wotd()
    render_display(data)