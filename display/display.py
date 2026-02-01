from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import json
import time

driver = None
durations = None
urls = None

def setup():
    global driver, durations, urls
    
    # Configure Chrome Options for Kiosk Mode
    options = Options()
    options.add_argument("--kiosk")
    options.add_argument("--no-sandbox")  
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-infobars")
    options.add_argument("--start-maximized")
    
    service = Service(executable_path="/usr/bin/chromedriver")
    
    driver = webdriver.Chrome(service=service, options=options)
    
    with open("config_configured.json", "r") as f:
        raw_config = f.read()
    config = json.loads(raw_config)
    urls = [x["url"] for x in config["urls"]]
    durations = [x["duration"] for x in config["urls"]]
    
    # Open two tabs for rotating content
    driver.get(urls[0])
    driver.execute_script("window.open('');") # Open new tab
    driver.switch_to.window(driver.window_handles[1])
    driver.get(urls[1])
    
    driver.switch_to.window(driver.window_handles[0])

def main():
    length = len(urls)
    content_tabs = driver.window_handles
    
    while True:
        for i in range(length):
            time.sleep(durations[i])
            
            # Switch between the two tabs
            current_tab = driver.current_window_handle
            next_tab = content_tabs[0] if current_tab == content_tabs[1] else content_tabs[1]
            
            driver.switch_to.window(next_tab)
            driver.get(urls[(i+2) % length])

if __name__ == "__main__":
    setup()
    try:
        main()
    except Exception as e:
        print(f"Error occurred: {e}")
        if driver:
            driver.quit()
    except KeyboardInterrupt:
        if driver:
            driver.quit()