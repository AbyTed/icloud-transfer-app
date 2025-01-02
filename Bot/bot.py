from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from dotenv import load_dotenv

import time
import os


from .constants import ICLOUDWEBSITE, PHOTO_ICLOUD_PAGE
from .helper import move_folder

load_dotenv()


class Bot:

    def __init__(self, driver, username: str, password: str):
        self.driver = driver
        self.username = str(username)
        self.password = str(password)
        self.wait = WebDriverWait(self.driver, 10)
        self.action = ActionChains(self.driver)
    def login_into_icloud(self):
        """
        Logs into the iCloud website using the provided username and password.
        This method performs the following steps:
        1. Navigates to the iCloud website.
        2. Clicks the sign-in button.
        3. Switches to the authentication iframe.
        4. Enters the username and submits.
        5. Clicks the continue button to proceed to the password entry.
        6. Enters the password and submits.
        Note: This method includes several waits to ensure elements are present and clickable before interacting with them.
        Attributes:
            self.driver (WebDriver): The Selenium WebDriver instance.
            self.wait (WebDriverWait): The WebDriverWait instance for explicit waits.
            self.username (str): The iCloud account username.
            self.password (str): The iCloud account password.
        """

        self.driver.get(ICLOUDWEBSITE)

        sign_in_button = self.wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "ui-button.push.primary.sign-in-button")
            )
        )
        sign_in_button.click()

        iframe = self.wait.until(
            EC.presence_of_element_located((By.ID, "aid-auth-widget-iFrame"))
        )

        # Switch to the iframe
        self.driver.switch_to.frame(iframe)

        login_box = self.wait.until(
            EC.presence_of_element_located((By.ID, "account_name_text_field"))
        )
        login_box.send_keys(self.username)
        
        time.sleep(1)
        
        login_box.send_keys(Keys.ENTER)
        try:
            
            continue_password = self.wait.until(
                EC.presence_of_element_located((By.ID, "continue-password"))
            )
            continue_password.click()
        except Exception as e:
            print(e)

        password_box = self.wait.until(
            EC.presence_of_element_located((By.ID, "password_text_field"))
        )

        password_box.send_keys(self.password)
        password_box.send_keys(Keys.ENTER)

        try:
            self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "error"))
            )
            return False
        except Exception as e:
            print("login is correct")
            return True
            
    def two_step_verification(self, code: str):
        code_list = list(code)

        inputs = self.wait.until(
            EC.presence_of_all_elements_located(
                (By.CLASS_NAME, "form-security-code-input")
            )
        )

        # Loop through each input and send the value '0'
        for i, input_element in enumerate(inputs):

            input_element.send_keys(code_list[i])

        not_now_button = self.wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "button.button.button-secondary.button-rounded-rectangle")
            )
        )

        not_now_button.click()

    def go_to_icloud(self) -> bool:
        try:
            self.driver.get(PHOTO_ICLOUD_PAGE)
            return True
        except Exception as e:
            print(f"Error is {e}")
            print("user does not have photo icloud page")
            return False

    def select_amount_of_photos_to_transfer(self, count, file_path):
        
        self.driver.get(PHOTO_ICLOUD_PAGE)
        
        iframe = self.wait.until(EC.presence_of_element_located((By.ID, "early-child")))

        # Switch to the iframe
        self.driver.switch_to.frame(iframe)

        photoButtonsList = self.wait.until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, ".PhotoItemView ")
            )
        )

        # Print the elements or their text content
        for index, element in enumerate(photoButtonsList, start=1):
            print(f"Element {index}: {element.text}")
        
        for _ in range(count):
            self.action.move_to_element(photoButtonsList[_]).key_down(Keys.SHIFT).click(photoButtonsList[_]).perform()

        download_button = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    ".DownloadButton",
                )
            )
        )
        download_button.click()

        move_folder(file_path)
        
        

    def close_driver(self):
        self.driver.quit()
