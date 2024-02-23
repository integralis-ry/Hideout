from selenium import webdriver
import json
import time

driver = None


def setup():
    global driver

    service = webdriver.ChromeService(executable_path="/usr/lib/chromium-browser/chromedriver")
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--kiosk")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    driver = webdriver.Chrome(service=service, options=options)

    with open("config.json", "r") as f:
        raw_config = f.read()
    config = json.loads(raw_config)
    urls = config["urls"]

    for url in urls:
        driver.get(url)
        driver.switch_to.new_window("tab")
    driver.close()


def main():
    while True:
        for window_handle in driver.window_handles:
            driver.switch_to.window(window_handle)
            time.sleep(10)


if __name__ == "__main__":
    setup()
    main()
