import customtkinter as ctk
import threading
import time

from .constants import AppConfig
from .utils import select_file, form_transfer_photo
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
            self,
            text="Home",
            font=appconfig.FONT_TITLE,
            text_color=appconfig.COLOR_TEXT,
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

        self.progressbar = ctk.CTkProgressBar(self, width=300, height=20)
        self.progressbar.grid(row=6, column=1, padx=20, pady=20)
        self.progress_var_num = ctk.DoubleVar()
        self.progressbar.configure(variable=self.progress_var_num)

    def icloud_photo_transfer(self):

        bot: Bot = self.controller.bot
        bot.transfer_name = self.transfer_name_entry.get()
        if self.progress_var.get():
            self.start_progress()
        for i in range(1):
            print(self.progress_var_num.get())
            time.sleep(1)
           
        bot.select_amount_of_photos_to_transfer(
            self.folder_name,
            delete=self.delete_var.get(),
        )

    def start_progress(self):
        """Start a new thread to run the progress bar update"""
        print("wo")

        def update_progress():
            for i in range(101):  # Loop from 0 to 100
                time.sleep(2)
                print(i)
                self.after(0, self.update_progress_bar, i)

        # Start the update function in a new thread
        threading.Thread(target=update_progress, daemon=True).start()

    def browse_folder(self):
        self.folder_name = select_file()
        self.browse_button.configure(text=self.folder_name)

    def go_to_settings(self):
        self.controller.show_frame("Setting")

    def update_progress_bar(self, value):
        """Update progress bar UI"""
        self.progress_var_num.set(value/1000)

    def go_to_history(self):
        self.controller.show_frame("History")
