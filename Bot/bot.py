from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver

from dotenv import load_dotenv

import time
import os

from .constants import ICLOUDWEBSITE, PHOTO_ICLOUD_PAGE
from .helper import move_folder, scroll_until_all_loaded

load_dotenv()


class Bot:

    def __init__(self, driver: WebDriver, username: str, password: str):
        self.driver = driver
        self.username = str(username)
        self.password = str(password)
        self.wait = WebDriverWait(self.driver, 10)
        self.action = ActionChains(self.driver)

    def login_into_icloud(self):
        self.driver.get(ICLOUDWEBSITE)

        try:
            sign_in_button = self.wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "ui-button.push.primary.sign-in-button")
                )
            )
            sign_in_button.click()
        except Exception as e:
            print(f"Error clicking sign-in button: {e}")

        try:
            iframe = self.wait.until(
                EC.presence_of_element_located((By.ID, "aid-auth-widget-iFrame"))
            )
            self.driver.switch_to.frame(iframe)
        except Exception as e:
            print(f"Error switching to iframe: {e}")

        try:
            login_box = self.wait.until(
                EC.presence_of_element_located((By.ID, "account_name_text_field"))
            )
            login_box.send_keys(self.username)
            time.sleep(1)
            login_box.send_keys(Keys.ENTER)
        except Exception as e:
            print(f"Error entering username: {e}")
            return False

        try:
            continue_password = self.wait.until(
                EC.presence_of_element_located((By.ID, "continue-password"))
            )
            continue_password.click()
        except Exception as e:
            print(f"Error clicking continue button: {e}")
            return False

        try:
            password_box = self.wait.until(
                EC.presence_of_element_located((By.ID, "password_text_field"))
            )
            password_box.send_keys(self.password)
            password_box.send_keys(Keys.ENTER)
        except Exception as e:
            print(f"Error entering password: {e}")
            return False
        try:

            self.wait.until(
                EC.presence_of_all_elements_located(
                    (By.CLASS_NAME, "form-security-code-input")
                )
            )
            return True
        except Exception as e:
            print("failed")
            return False

    def two_step_verification(self, code: str):
        code_list = list(code)

        inputs = self.wait.until(
            EC.presence_of_all_elements_located(
                (By.CLASS_NAME, "form-security-code-input")
            )
        )

        for i, input_element in enumerate(inputs):
            input_element.send_keys(code_list[i])

        try:
            not_now_button = self.wait.until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        "button.button.button-secondary.button-rounded-rectangle",
                    )
                )
            )
            not_now_button.click()
        except Exception as e:
            print(f"Error clicking 'Not Now' button: {e}")

    def go_to_icloud(self) -> bool:
        try:
            self.driver.get(PHOTO_ICLOUD_PAGE)
            return True
        except Exception as e:
            print(f"Error is {e}")
            print("user does not have photo icloud page")
            return False

    def select_amount_of_photos_to_transfer(
        self, count: int, file_path: str, delete: bool, progress_bar: bool
    ):
        self.driver.get(PHOTO_ICLOUD_PAGE)
        try:

            iframe = self.wait.until(
                EC.presence_of_element_located((By.ID, "early-child"))
            )

            self.driver.switch_to.frame(iframe)
        except Exception as e:
            print(f"Error when switching icloud iframe {e}")

        photo_css = ".PhotoItemView"
        grid_css = ".grid-items"
        scroll_until_all_loaded(
            self, self.driver, container_css=grid_css, item_css=photo_css, delete=delete
        )

        try:
            download_button = self.wait.until(
                EC.element_to_be_clickable(
                    (
                        By.CSS_SELECTOR,
                        ".DownloadButton",
                    )
                )
            )
            download_button.click()

        except Exception as e:
            print(f"Error clicking download button: {e}")
        if delete:
            try:
                self.wait.until(
                    EC.invisibility_of_element_located(
                        (By.CSS_SELECTOR, ".FullPageSpinnerContainer")
                    )
                )
                self.driver.execute_script("document.body.click();")
                # Wait for the delete button to be clickable (adds a bit of reliability)
                delete_button = self.wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, ".DeleteButton"))
                )

                # Move to the element and perform the click
                delete_button.click()
                # Wait for the delete button to be clickable
                delete_button = self.wait.until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, "ui-button.block.large.secondary.destructive")
                    )
                )

                # Perform the click action
                self.action.move_to_element(delete_button).click(
                    delete_button
                ).perform()
            except Exception as e:
                print(f"Error clicking delete button: {e}")
        move_folder(file_path)

    def close_driver(self):
        self.driver.quit()
