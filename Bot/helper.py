import os
import zipfile
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def move_folder(file_path: str):
    """
    Moves the most recent zip file from the Downloads folder to the specified file path and extracts its contents.

    Args:
        file_path: The destination directory where the contents of the zip file will be extracted.

    Returns:
        None
    """
    downloads_path = os.path.join(os.environ["USERPROFILE"], "Downloads")

    items = [os.path.join(downloads_path, f) for f in os.listdir(downloads_path)]

    items.sort(key=lambda x: os.path.getmtime(x), reverse=True)

    most_recent_file = items[0]

    if most_recent_file.endswith(".zip"):
        print(f"Most recent zip file: {most_recent_file}")

        with zipfile.ZipFile(most_recent_file, "r") as zip_ref:
            zip_ref.extractall(file_path)

        print(f"Contents of the zip file extracted to: {file_path}")

        os.remove(most_recent_file)
    else:
        time.sleep(3)

        move_folder(file_path)


def scroll_until_all_loaded(
    self, driver: WebDriver, container_css: str, item_css: str, delete: bool
) -> list[WebElement]:
    """
    Scrolls a container dynamically until all items are loaded.

    Args:
        driver: The Selenium WebDriver instance.
        container_css: XPath of the scrollable container.
        item_css: css of the items within the container.

    Returns:
        List of WebElements (all loaded items).
    """
    
    retries = 0
    items = list()
    
    while retries < 1000:  # Allow up to 3 retries for edge cases
        try:

            # Get the current number of items
            items = driver.find_elements(By.CSS_SELECTOR, item_css)
            current_item_count = len(set(items))

            # If no new items are loaded, increment retries

            retries += current_item_count
            print(retries)
            if items:
                cur_items = [items[0], items[-1]]
                for item in cur_items:

                    try:
                        self.action.move_to_element(item).key_down(Keys.SHIFT).click(
                            item
                        ).perform()
                        time.sleep(1)
                    except Exception as e:
                        print(f"Error when selecting photos {e}")

                time.sleep(1)  # Short delay to allow items to load
            else:
                print("no items")
        except Exception as e:
            print(f"Error during clicking: {e}")
            break
        
    if delete:
        try:
            delete_button = self.wait.until(
                EC.element_to_be_clickable(
                    (
                        By.CSS_SELECTOR,
                        ".DeleteButton",
                    )
                )
            )
            delete_button.click()
        except Exception as e:
            print(f"Error clicking delete button: {e}")
    self.action.click(items[0]).perform()
