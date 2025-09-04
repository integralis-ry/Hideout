import time
import json
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Load configuration
with open("config.json") as f:
    config = json.load(f)

# Configure Chromium to run in kiosk mode
chrome_options = Options()

# Find Chromium binary path
chromium_path = shutil.which('chromium-browser') or shutil.which('chromium')
if chromium_path:
    chrome_options.binary_location = chromium_path
else:
    print("Chromium not found. Please install Chromium.")
    exit(1)

chrome_options.add_argument("--kiosk")
chrome_options.add_experimental_option("detach", True)  # Keep browser open after script ends

# Initialize the browser with Chromium
driver = webdriver.Chrome(options=chrome_options)

try:
    while True:
        for entry in config["urls"]:
            url, duration = entry["url"], entry["duration"]
            driver.get(url)  # Navigate to URL in existing tab
            time.sleep(duration)
finally:
    driver.quit()  # Proper cleanup when program ends