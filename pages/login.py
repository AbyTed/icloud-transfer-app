import customtkinter as ctk
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from Bot import Bot
from .utils import create_popup_entry

from .constants import COLOR_TEXT, FONT_SECONDARY, ENTRY_TEXT_COLOR, ENTRY_COLOR, FONT_TITLE, COLOR_ERROR

class Login(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)

        self.controller = controller

        # Label for "Login"
        label = ctk.CTkLabel(self, text="Login", font=FONT_TITLE, text_color = COLOR_TEXT )
        label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Label and Entry for Username
        username_label = ctk.CTkLabel(self, text="Username:", font=FONT_SECONDARY, text_color=COLOR_TEXT)
        username_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        
        self.username_entry = ctk.CTkEntry(self, fg_color=ENTRY_COLOR, text_color=ENTRY_TEXT_COLOR)
        self.username_entry.grid(row=1, column=1, padx=10, pady=10)

        # Label and Entry for Password
        password_label = ctk.CTkLabel(self, text="Password:", font=FONT_SECONDARY, text_color=COLOR_TEXT)
        password_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        
        self.password_entry = ctk.CTkEntry(self, show="*", fg_color=ENTRY_COLOR, text_color=ENTRY_TEXT_COLOR)  # Hides password characters
        self.password_entry.grid(row=2, column=1, padx=10, pady=10)

        # Login Button
        login_button = ctk.CTkButton(self, text="Login", command=self.login, )
        login_button.grid(row=3, column=0, columnspan=2, pady=10)

        # error label
        self.error_label = ctk.CTkLabel(self, text="Your Username or Password is incorrect. Please type it again.", text_color=COLOR_ERROR)
        self.error_label.pack_forget()

        
        self.logging_in = ctk.CTkLabel(self, text="Logining", text_color=COLOR_ERROR)
        self.logging_in.pack_forget()
        
    def login_wrong_prompt(self):
        self.error_label.grid(row=4, column=0, columnspan=2, pady=10)
    
    def logging_in_screen(self):
        self.logging_in.grid(row=4, column=0, columnspan=2, pady=10)
      
    def login(self):
        """
        Logs the user into iCloud using the provided username and password.
        This method retrieves the username and password from the entry boxes,
        validates them, initializes the Bot class, and performs the login process.
        If two-step verification is required, it prompts the user to enter the
        verification code and completes the verification.
        Steps:
        1. Retrieve username and password from entry boxes.
        2. Validate that username and password are not empty.
        3. Initialize the Bot class with the username and password.
        4. Perform the login using the Bot class.
        5. Prompt the user for the two-step verification code.
        6. Complete the two-step verification using the provided code.
        Returns:
            None
        """
        # remove error message if any
        self.error_label.pack_forget()
        
        # Get the username and password as strings from the entry boxes
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Ensure the username and password are valid strings (you can add extra validation here if necessary)
        if not username or not password:
            print("Username and password cannot be empty.")
            return

        # Initialize the Bot class with the correct parameters
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # you won't be able to see the browser
        chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration (saves gpu power)

        # Create the WebDriver with the options
        driver = webdriver.Chrome(options=chrome_options)
        
        self.controller.bot = Bot(webdriver.Chrome(), username, password)
        
        
        
        if not self.controller.bot.login_into_icloud():
            self.login_wrong_prompt()
        else:
            # Create the popup entry for the two-step verification code
            code = "placeholder"
            while not code.isdigit() or len(code) != 6:
                code = create_popup_entry()

            # Pass the code to the bot for two-step verification
            self.controller.bot.two_step_verification(code)

            self.go_to_home()
           
    def go_to_home(self):
        self.controller.show_frame('Home')
        
