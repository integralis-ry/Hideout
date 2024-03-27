from selenium import webdriver
import json
import time

driver = None
durations = None


def setup():
    global driver
    global durations

    service = webdriver.FirefoxService(executable_path="/snap/bin/geckodriver")
    options = webdriver.FirefoxOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--kiosk")
    driver = webdriver.Firefox(service=service, options=options)

    with open("config_configured.json", "r") as f:
        raw_config = f.read()
    config = json.loads(raw_config)
    urls = [x["url"] for x in config["urls"]]
    durations = [x["duration"] for x in config["urls"]]

    for url in urls:
        driver.get(url)
        driver.switch_to.new_window("tab")
    driver.close()


def main():
    while True:
        for duration, window_handle in zip(durations, driver.window_handles):
            driver.switch_to.window(window_handle)
            time.sleep(duration)


if __name__ == "__main__":
    setup()
    try:
        main()
    except KeyboardInterrupt:
        driver.quit()
