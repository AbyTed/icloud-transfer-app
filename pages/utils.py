import customtkinter as ctk
from customtkinter import filedialog

from .constants import AppConfig

def create_popup_entry() -> str:
    """
    Creates a popup window to prompt the user to enter a verification code.
    
    Returns:
        str: The verification code entered by the user.
    """
    popup = ctk.CTkToplevel()
    popup.title("Enter your code")
    popup.geometry("300x200")

    user_input_val = ctk.StringVar()

    label = ctk.CTkLabel(popup, text="Please enter verification code from Apple:")
    label.pack(padx=10, pady=10)

    entry = ctk.CTkEntry(
        popup, placeholder_text="Enter Code", textvariable=user_input_val
    )
    entry.pack(padx=10, pady=10)

    def submit():
        popup.destroy()

    submit_button = ctk.CTkButton(popup, text="Submit", command=submit)
    submit_button.pack(pady=10)

    popup.wait_window()

    return user_input_val.get()

def select_file():
    """
    Opens a file dialog for the user to select a folder.
    
    Returns:
        str: The path of the selected folder, or None if no folder was selected.
    """
    folder_path = filedialog.askdirectory(title="Select Folder")
    if folder_path:
        return folder_path
    return None

def form_transfer_photo(self):
    """
    Creates the form for transferring photos, including input fields and options.
    """
    appconfig = AppConfig()

    # Transfer name input
    self.transfer_name_label = ctk.CTkLabel(self, text="Transfer Name:", text_color=appconfig.COLOR_TEXT)
    self.transfer_name_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

    self.transfer_name_entry = ctk.CTkEntry(self, text_color=appconfig.COLOR_TEXT)
    self.transfer_name_entry.grid(row=0, column=1, padx=10, pady=5)

    # Folder location input
    self.folder_label = ctk.CTkLabel(self, text="Folder Location:", text_color=appconfig.COLOR_TEXT)
    self.folder_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    self.browse_button = ctk.CTkButton(self, text="Browse", command=self.browse_folder, text_color=appconfig.COLOR_TEXT)
    self.browse_button.grid(row=1, column=1, padx=10, pady=5)

    # Progress option (progress bar)
    self.progress_var = ctk.BooleanVar()
    self.progress_checkbox = ctk.CTkCheckBox(
        self, text="Progress bar for transfer", variable=self.progress_var, text_color=appconfig.COLOR_TEXT
    )
    self.progress_checkbox.grid(row=3, column=0, padx=10, pady=5, columnspan=1)

    # Delete option
    self.delete_var = ctk.BooleanVar()
    self.delete_checkbox = ctk.CTkCheckBox(
        self, text="Delete photos after transfer", variable=self.delete_var, text_color=appconfig.COLOR_TEXT
    )
    self.delete_checkbox.grid(
        row=4, column=0, columnspan=2, padx=10, pady=10, sticky="w"
    )

    # Transfer button
    self.transfer_button = ctk.CTkButton(
        self,
        text="Transfer Photos",
        font=appconfig.FONT_PRIMARY,
        text_color=appconfig.COLOR_TEXT,
        fg_color=appconfig.BUTTON_COLOR,
        hover_color=appconfig.BUTTON_HOVER,
        command=self.icloud_photo_transfer,
    )
    self.transfer_button.grid(row=5, column=0, columnspan=3, padx=20, pady=20)
