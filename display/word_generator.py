import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

def get_wotd():
    options = Options()
    options.add_argument("--headless") # Headless is fine if we wait for the right elements
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # Force a standard window size so elements aren't hidden
    options.add_argument("--window-size=1920,1080")

    service = Service(executable_path="/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)
    
    # We use the specific phrases page to avoid the quiz popup
    url = "https://www.finnishpod101.com/finnish-phrases/"
    
    try:
        driver.get(url)
        
        # 1. WAIT for the actual word content, not just the page load
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "wotd-item-word")))
        
        # 2. SCROLL just in case (optional but helps some dynamic sites)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/4);")
        time.sleep(2) 

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # 3. EXTRACTION (Using specific classes from your images)
        word = soup.find(class_='wotd-item-word').get_text(strip=True)
        meaning = soup.find(class_='wotd-item-meaning').get_text(strip=True)

        examples_html = ""
        # The dynamic loop handles whatever number of examples exist
        example_items = soup.find_all(class_='wotd-example-item')
        
        for item in example_items[:4]: # Limit to 4 for screen space
            fi = item.find(class_='wotd-example-sentence').get_text(strip=True)
            en = item.find(class_='wotd-example-meaning').get_text(strip=True)
            examples_html += f"""
            <div class="example-item">
                <span class="fi-text">{fi}</span>
                <span class="en-text">{en}</span>
            </div>
            """
            
        return {'word': word, 'meaning': meaning, 'examples_html': examples_html}

    except Exception as e:
        print(f"Scraper failed: {e}")
        return None
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