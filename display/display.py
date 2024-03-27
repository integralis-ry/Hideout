from selenium import webdriver
import json
import time

driver = None
durations = None
urls = None

def setup():
    global driver
    global durations
    global urls

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

    driver.get(urls[0])
    driver.switch_to.new_window("tab")
    driver.get(urls[1])
    driver.switch_to.window(driver.window_handles[0])


def main():
    length = len(urls)
    while True:
        for i in range(length):
            time.sleep(durations[i])
            driver.get(urls[(i+2)%length])
            driver.switch_to.window(driver.window_handles[(i+1)%2])


if __name__ == "__main__":
    setup()
    try:
        main()
    except KeyboardInterrupt:
        driver.quit()
