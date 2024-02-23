from selenium import webdriver
import json

driver = None
URL = None


def setup():
    global URL
    global driver

    service = webdriver.ChromeService(executable_path='/usr/lib/chromium-browser/chromedriver')
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=service, options=options)

    with open("config.json", "r") as f:
        raw_config = f.read()
    config = json.loads(raw_config)
    URL = config["URL"]


def main():
    driver.get(URL)


if __name__ == "__main__":
    setup()
    main()
    while True:
        pass
