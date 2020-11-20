from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common import exceptions

import json


def parse_json(json_file_path):
    with open(json_file_path, 'r') as json_file:
        dictionary = json.load(json_file)
        return dictionary

class SporkInstance:
    def __init__(self, driver_path, is_headless, json_creds_path= "creds.json"):
        if is_headless:
            option = webdriver.ChromeOptions()
            option.add_argument('headless')
        else: option = None
        self.driver = webdriver.Chrome(driver_path, options=option)
        self.driver.get('https://spork.school/schedule')
        self.credentials = parse_json(json_creds_path)


    def enter_credentials(self):
        try:
            usernameField = WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.NAME, "username")))
            usernameField.send_keys(self.credentials.get("username"))
            
            passwordField = WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.NAME, "password")))
            passwordField.send_keys(self.credentials.get("password"))
            passwordField.send_keys(Keys.ENTER)
        except (exceptions.NoSuchElementException, exceptions.TimeoutException):
            self.driver.quit()

    def click_join_button(self):
        try:
            joinButton = WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.CSS_SELECTOR, 'button.ui.green.compact.button')))
            joinButton.click()
        except (exceptions.NoSuchElementException, exceptions.TimeoutException):
            print("no button")
            self.driver.quit()

if __name__ == "__main__":
    client = SporkInstance("chromedriver.exe", False, "creds.json")
    client.enter_credentials()
    client.click_join_button()
