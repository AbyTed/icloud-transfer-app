import customtkinter as ctk
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import threading
import webbrowser

from Bot import Bot
from .utils import create_popup_entry

from .constants import AppConfig
from .frame_helper import FrameHelper


class Login(ctk.CTkFrame, FrameHelper):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)

        self.controller = controller
        self.initialize_ui()

    def initialize_ui(self):
        """
        Initializes the user interface for the login page, including labels, entry fields, and buttons.
        """
        appconfig = AppConfig()

        # Label for "Login"
        label = ctk.CTkLabel(
            self,
            text="Login",
            font=appconfig.FONT_TITLE,
            text_color=appconfig.COLOR_TEXT,
        )
        label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Label and Entry for Username
        username_label = ctk.CTkLabel(
            self,
            text="Username:",
            font=appconfig.FONT_SECONDARY,
            text_color=appconfig.COLOR_TEXT,
        )
        username_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")

        self.username_entry = ctk.CTkEntry(
            self, fg_color=appconfig.ENTRY_COLOR, text_color=appconfig.ENTRY_TEXT_COLOR
        )
        self.username_entry.grid(row=1, column=1, padx=10, pady=10)

        # Label and Entry for Password
        password_label = ctk.CTkLabel(
            self,
            text="Password:",
            font=appconfig.FONT_SECONDARY,
            text_color=appconfig.COLOR_TEXT,
        )
        password_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")

        self.password_entry = ctk.CTkEntry(
            self,
            show="*",
            fg_color=appconfig.ENTRY_COLOR,
            text_color=appconfig.ENTRY_TEXT_COLOR,
        )  # Hides password characters
        self.password_entry.grid(row=2, column=1, padx=10, pady=10)

        # Login Button
        login_button = ctk.CTkButton(
            self,
            text="Login",
            command=self.login,
        )
        login_button.grid(row=3, column=0, columnspan=2, pady=10)

        # sign up Button
        sign_up_button = ctk.CTkButton(
            self,
            text="Sign Up",
            command=self.sign_up,
        )
        sign_up_button.grid(row=3, column=4, columnspan=2, pady=10)
        # error label
        self.error_label = ctk.CTkLabel(
            self,
            text="Your Username or Password is incorrect. Please type it again.",
            text_color=appconfig.COLOR_ERROR,
        )
        self.error_label.grid_forget()

        self.logging_label = ctk.CTkLabel(
            self,
            font=appconfig.LARGE_FONT,
            text="Logging in",
            text_color=appconfig.COLOR_HIGHLIGHT,
        )
        self.logging_label.grid_forget()

    def login_wrong_prompt(self):
        """
        pops up a text that tells the user that they have typed in the wrong login
        """
        self.error_label.grid(row=4, column=0, columnspan=2, pady=10)

    def logging_in_screen(self, onOff: bool = True):
        """
        Plays a logging-in animation with 'Logging in.', 'Logging in..', 'Logging in...'.
        """
        # Check if we're stopping the animation
        if not onOff:
            if hasattr(self, "animation_id"):
                self.after_cancel(self.animation_id)  # Cancel the scheduled task
                del self.animation_id  # Clean up the attribute
            self.logging_label.grid_forget()  # Hide the label
            return  # Stop the function

        # Show the label
        self.logging_label.grid(row=5, column=0, columnspan=2, pady=10)

        # Update the label's text
        current_text = self.logging_label.cget("text")
        if current_text.endswith("..."):
            self.logging_label.configure(text="Logging in")
        else:
            self.logging_label.configure(text=current_text + ".")

        # Schedule the function to run again after 500ms and save the callback ID
        self.animation_id = self.after(500, self.logging_in_screen)

    def sign_up(self):
        """
        tries to open a new window or new tab by using the default browser and open up apple.com sign up page
        """
        URL = "https://account.apple.com/account"
        webbrowser.open_new(URL)

    def login(self):

        # Get the username and password as strings from the entry boxes
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Ensure the username and password are valid strings (you can add extra validation here if necessary)
        if not username or not password:
            print("Username and password cannot be empty.")
            return
        # remove error message if any
        self.error_label.grid_forget()
        self.logging_in_screen(True)

        def bot_login_process():
            try:

                # Initialize the Bot class with the correct parameters
                chrome_options = Options()
                chrome_options.add_argument(
                    "--headless"
                )  # you won't be able to see the browser
                chrome_options.add_argument(
                    "--disable-gpu"
                )  # Disable GPU acceleration (saves gpu power)

                # Create the WebDriver with the options
                driver = webdriver.Chrome(options=chrome_options)

                self.controller.bot = Bot(webdriver.Chrome(), username, password)

                if not self.controller.bot.login_into_icloud():
                    self.controller.bot.close_driver()
                    self.login_wrong_prompt()
                    self.logging_in_screen(onOff=False)
                else:
                    # Create the popup entry for the two-step verification code
                    code = "placeholder"
                    while not code.isdigit() or len(code) != 6:
                        code = create_popup_entry()

                    # Pass the code to the bot for two-step verification
                    self.controller.bot.two_step_verification(code)

                    self.go_to_home()
            except Exception as e:
                print(f"login process error: {e}")

        bot_thread = threading.Thread(target=bot_login_process, daemon=True)
        bot_thread.start()

    def go_to_home(self):
        self.controller.show_frame("Home")
