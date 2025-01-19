import customtkinter as ctk

from .constants import AppConfig
from .utils import select_file, form_transfer_photo
from Bot import Bot
from .frame_helper import FrameHelper


class Home(ctk.CTkFrame, FrameHelper):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)

        self.controller = controller
        self.initialize_ui()

    def initialize_ui(self):
        # Title Label
        appconfig = AppConfig()

        label = ctk.CTkLabel(
            self, text="Home", font=appconfig.FONT_TITLE, text_color=appconfig.COLOR_TEXT
        )
        label.grid(row=0, column=1, padx=10, pady=20, sticky="n")

        form_transfer_photo(self)

        # Button for settings
        settings_button = ctk.CTkButton(
            self,
            text="Settings",
            font=appconfig.FONT_PRIMARY,
            text_color=appconfig.COLOR_TEXT,
            fg_color=appconfig.BUTTON_COLOR,
            hover_color=appconfig.BUTTON_HOVER,
            command=lambda: self.go_to_settings(),
        )
        settings_button.grid(row=1, column=2, padx=20, pady=20, sticky="e")

        history_button = ctk.CTkButton(
            self,
            text="History",
            font=appconfig.FONT_PRIMARY,
            text_color=appconfig.COLOR_TEXT,
            fg_color=appconfig.BUTTON_COLOR,
            hover_color=appconfig.BUTTON_HOVER,
            command=lambda: self.go_to_history(),
        )
        history_button.grid(row=2, column=2, padx=20, pady=20, sticky="e")
    def icloud_photo_transfer(self):

        bot: Bot = self.controller.bot
        bot.transfer_name = self.transfer_name_entry.get()
        bot.select_amount_of_photos_to_transfer(
            1000,
            self.folder_name,
            delete=self.delete_var.get(),
            progress_bar=self.progress_var.get(),
        )

    def browse_folder(self):
        self.folder_name = select_file()
        self.browse_button.configure(text=self.folder_name)

    def go_to_settings(self):
        self.controller.show_frame("Setting")
    def go_to_history(self):
        self.controller.show_frame("History")