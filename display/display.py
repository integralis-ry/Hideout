from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import json
import time

driver = None
config_data = [] # Store the full dict for easier access

def apply_zoom(zoom_level):
    """Applies the zoom level to the current page via JavaScript."""
    try:
        # Most modern browsers support style.zoom; alternatively use transform
        driver.execute_script(f"document.body.style.zoom='{zoom_level}'")
    except Exception as e:
        print(f"Could not apply zoom: {e}")

def setup():
    global driver, config_data
    
    options = Options()
    options.add_argument("--kiosk")
    options.add_argument("--no-sandbox")  
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-infobars")
    
    service = Service(executable_path="/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)
    
    with open("config_configured.json", "r") as f:
        config = json.load(f)
        config_data = config["urls"]
    
    # Initialize the first two tabs
    driver.get(config_data[0]["url"])
    apply_zoom(config_data[0].get("zoom", 1)) # Initial zoom
    
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    
    driver.get(config_data[1]["url"])
    apply_zoom(config_data[1].get("zoom", 1)) # Initial zoom
    
    driver.switch_to.window(driver.window_handles[0])

def main():
    length = len(config_data)
    content_tabs = driver.window_handles
    
    while True:
        for i in range(length):
            # 1. Wait for the duration of the CURRENT visible page
            time.sleep(config_data[i]["duration"])
            
            # 2. Identify the tab we are moving TO
            current_tab = driver.current_window_handle
            next_tab = content_tabs[0] if current_tab == content_tabs[1] else content_tabs[1]
            
            # 3. Switch to the next tab
            driver.switch_to.window(next_tab)
            
            # 4. Determine the index of the next content to load in the BACKGROUND
            # (i+2) because we are already showing 'i', 'i+1' is in the other tab.
            next_content_idx = (i + 2) % length
            next_url = config_data[next_content_idx]["url"]
            next_zoom = config_data[next_content_idx].get("zoom", 1)
            
            # 5. Load the next URL and apply its specific zoom level
            driver.get(next_url)
            apply_zoom(next_zoom)

if __name__ == "__main__":
    setup()
    try:
        main()
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        if driver:
            driver.quit()