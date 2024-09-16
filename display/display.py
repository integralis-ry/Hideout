from selenium import webdriver
import json
import time

driver = None
durations = None
urls = None
calendar_tab = None

def setup():
    global driver, durations, urls, calendar_tab
    service = webdriver.FirefoxService(executable_path="/snap/bin/geckodriver")
    options = webdriver.FirefoxOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--kiosk")
    options.page_load_strategy = "none"
    driver = webdriver.Firefox(service=service, options=options)

    with open("config_configured.json", "r") as f:
        raw_config = f.read()
    config = json.loads(raw_config)
    urls = [x["url"] for x in config["urls"]]
    durations = [x["duration"] for x in config["urls"]]

    # Pre-load the calendar page in a separate tab
    driver.get("https://www.integralis.fi/calendar")
    calendar_tab = driver.current_window_handle

    # Open two more tabs for rotating content
    driver.switch_to.new_window("tab")
    driver.get(urls[0])
    driver.switch_to.new_window("tab")
    driver.get(urls[1])

    # Switch back to the first content tab
    driver.switch_to.window(driver.window_handles[1])

def main():
    global calendar_tab
    length = len(urls)
    content_tabs = [handle for handle in driver.window_handles if handle != calendar_tab]
    
    while True:
        for i in range(length):
            time.sleep(durations[i])
            
            # Check if the current URL is the calendar URL
            if urls[(i+2)%length] == "https://www.integralis.fi/calendar":
                driver.switch_to.window(calendar_tab)
            else:
                current_tab = driver.current_window_handle
                next_tab = content_tabs[0] if current_tab == content_tabs[1] else content_tabs[1]
                driver.switch_to.window(next_tab)
                driver.get(urls[(i+2)%length])

            # Refresh the calendar tab periodically (e.g., every 5 minutes)
            if i % (300 // min(durations)) == 0:  # Adjust this condition as needed
                original_tab = driver.current_window_handle
                driver.switch_to.window(calendar_tab)
                driver.refresh()
                driver.switch_to.window(original_tab)

if __name__ == "__main__":
    setup()
    try:
        main()
    except KeyboardInterrupt:
        driver.quit()
