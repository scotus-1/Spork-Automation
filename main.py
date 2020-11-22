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
            usernameField.clear()
            usernameField.send_keys(self.credentials.get("username"))
            
            passwordField = WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.NAME, "password")))
            passwordField.clear()
            passwordField.send_keys(self.credentials.get("password"))
            passwordField.send_keys(Keys.ENTER)
            
            #returns true if the login is no longer attached to the DOM, i.e. no longer there
            #else makes an error
            staleness = WebDriverWait(self.driver, 3).until(ec.staleness_of(passwordField))

            #whether to continue, as it would produce an error if it tried to use webdriver and it quit
            return True
        except (exceptions.NoSuchElementException, exceptions.TimeoutException):
            print("Unable to enter credentials")
            self.driver.quit()
            return False

    def click_join_button(self):
        try:
            joinButtons = WebDriverWait(self.driver, 10).until(ec.presence_of_all_elements_located((By.CSS_SELECTOR, 'button.ui.green.compact.button')))
            for button in joinButtons:
                button.click()
        except (exceptions.NoSuchElementException, exceptions.TimeoutException):
            print("No button to press")
            self.driver.quit()

if __name__ == "__main__":
    client = SporkInstance("chromedriver.exe", False, "creds.json")
    success = client.enter_credentials()
    if (success):
        client.click_join_button()
