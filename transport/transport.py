from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import json


def setup():
    service = webdriver.ChromeService(executable_path='/usr/lib/chromium-browser/chromedriver')
    driver = webdriver.Chrome(service=service)
    return driver


def main(driver):
    driver.get("http://www.python.org")


if __name__ == "__main__":
    driver = setup()
    main(driver)
