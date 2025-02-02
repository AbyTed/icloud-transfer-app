import os
import zipfile
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
import time


import os
import zipfile
import time


def move_folder(file_path: str, name_transfer: str, val=1):
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

        # Extract contents of the zip file
        with zipfile.ZipFile(most_recent_file, "r") as zip_ref:
            zip_ref.extractall(file_path)

        print(f"Contents of the zip file extracted to: {file_path}")

        # Assuming the extracted folder is the only folder in the destination path
        extracted_folder = os.path.join(file_path, os.listdir(file_path)[0])

        # Rename the extracted folder 
        new_folder_name = name_transfer
        new_folder_path = os.path.join(file_path, new_folder_name)

        if os.path.exists(extracted_folder):
            os.rename(extracted_folder, new_folder_path)
            print(f"Renamed folder from {extracted_folder} to {new_folder_path}")

        # Remove the zip file after extraction and renaming
        os.remove(most_recent_file)
    else:
        time.sleep(3 * val)
        val += 2
        move_folder(file_path, val=val, name_transfer=name_transfer)


def scroll_until_all_loaded(self, driver: WebDriver, item_css: str) -> list[WebElement]:

    retries = 0
    items = list()

    while retries < 1500:
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
