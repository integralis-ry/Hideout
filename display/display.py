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
    driver = webdriver.Firefox(service=service, options=options)

    with open("config_configured.json", "r") as f:
        raw_config = f.read()
    config = json.loads(raw_config)
    urls = [x["url"] for x in config["urls"]]
    durations = [x["duration"] for x in config["urls"]]
    #durations = durations[-1:] + durations[:-1]
    driver.get(urls[-1])


def main():
    while True:
        for url, duration in zip(urls, durations):
            driver.close()
            driver.switch_to.new_window("tab")
            driver.get(url)
            time.sleep(duration)


if __name__ == "__main__":
    setup()
    try:
        main()
    except KeyboardInterrupt:
        driver.quit()
