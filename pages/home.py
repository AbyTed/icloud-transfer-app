import customtkinter as ctk

from .constants import FONT_PRIMARY, COLOR_BACKGROUND, FONT_TITLE, COLOR_TEXT, BUTTON_COLOR, BUTTON_HOVER
from .utils import select_file
from Bot import Bot


class Home(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.configure(fg_color=COLOR_BACKGROUND)
        self.controller = controller
        # Title Label
        label = ctk.CTkLabel(self, text="Home", font=FONT_TITLE, text_color=COLOR_TEXT)
        label.grid(row=0, column=1, padx=10, pady=20, sticky="n")

        # Button to transfer photos
        transfer_button = ctk.CTkButton(
            self,
            text="Transfer Photos",
            font=FONT_PRIMARY,
            text_color=COLOR_TEXT,
            fg_color=BUTTON_COLOR,
            hover_color=BUTTON_HOVER,
            command=lambda: self.icloud_photo_transfer(),
        )
        transfer_button.grid(row=1, column=0, padx=20, pady=20, sticky="w")

        # Button for settings
        settings_button = ctk.CTkButton(
            self,
            text="Settings",
            font=FONT_PRIMARY,
            text_color=COLOR_TEXT,
            fg_color=BUTTON_COLOR,
            hover_color=BUTTON_HOVER,
            command=lambda: self.go_to_settings()
        )
        settings_button.grid(row=1, column=2, padx=20, pady=20, sticky="e")

    def icloud_photo_transfer(self):
        folder_name = select_file()

        bot: Bot = self.controller.bot

        bot.select_amount_of_photos_to_transfer(10, folder_name)
    
    def go_to_settings(self):
        self.controller.show_frame('Setting')