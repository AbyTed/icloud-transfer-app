import customtkinter as ctk
from tkinter import StringVar, IntVar

from .constants import AppConfig
from .frame_helper import FrameHelper


class Settings(ctk.CTkFrame, FrameHelper):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)

        self.controller = controller
        self.initialize_ui()

    def initialize_ui(self):
        appconfig = AppConfig()
        self.appconfig = AppConfig()
        # Label for "Settings"
        label = ctk.CTkLabel(
            self,
            text="Settings",
            font=appconfig.FONT_TITLE,
            text_color=appconfig.COLOR_TEXT,
        )
        label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Threading toggle option
        threading_label = ctk.CTkLabel(
            self,
            text="Enable Threading:",
            font=appconfig.FONT_TITLE,
            text_color=appconfig.COLOR_TEXT,
        )
        threading_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")

        self.threading_var = IntVar(value=int(appconfig.THREADING))
        threading_toggle = ctk.CTkSwitch(
            self, variable=self.threading_var, text="", command=self.toggle_threading
        )
        threading_toggle.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Theme options
        theme_label = ctk.CTkLabel(
            self,
            text="Theme:",
            font=appconfig.FONT_TITLE,
            text_color=appconfig.COLOR_TEXT,
        )
        theme_label.grid(row=3, column=0, padx=10, pady=10, sticky="e")

        self.theme_var = StringVar(value=str(ctk.get_appearance_mode()))
        theme_option_menu = ctk.CTkOptionMenu(
            self,
            values=["Dark", "Light"],
            variable=self.theme_var,
        )
        theme_option_menu.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        # Font type option
        font_label = ctk.CTkLabel(
            self,
            text="Font Type:",
            font=appconfig.FONT_TITLE,
            text_color=appconfig.COLOR_TEXT,
        )
        font_label.grid(row=4, column=0, padx=10, pady=10, sticky="e")

        self.font_var = StringVar(value=str(appconfig.FONT_PRIMARY[0]))
        font_option_menu = ctk.CTkOptionMenu(
            self,
            values=["Default", "Arial", "Courier", "Helvetica"],
            variable=self.font_var,
            
        )
        font_option_menu.grid(row=4, column=1, padx=10, pady=10, sticky="w")

        # Font color option
        font_color_label = ctk.CTkLabel(
            self,
            text="Font Color:",
            font=appconfig.FONT_TITLE,
            text_color=appconfig.COLOR_TEXT,
        )
        font_color_label.grid(row=5, column=0, padx=10, pady=10, sticky="e")

        self.font_color_var = StringVar(value=appconfig.COLOR_TEXT)
        font_color_option_menu = ctk.CTkOptionMenu(
            self,
            values=["Black", "White", "Red", "Blue", "Green"],
            variable=self.font_color_var,
            
        )
        font_color_option_menu.grid(row=5, column=1, padx=10, pady=10, sticky="w")

        # Save Button
        save_button = ctk.CTkButton(
            self,
            text="Save Settings",
            command=self.save_settings,
        )
        save_button.grid(row=6, column=0, columnspan=2, pady=10)

        #exit to home
        home_button = ctk.CTkButton(
            self,
            text="Back",
            command=self.go_to_home,
        )
        home_button.grid(row=6, column = 2, columnspan=2, pady=10)
    
    def toggle_threading(self):
        self.appconfig.save_threading(self.threading_var.get())

    def toggle_scrollbar(self):
        if self.scrollbar_var.get():
            print("Scrollbar enabled.")
        else:
            print("Scrollbar disabled.")
    def go_to_home(self):
        self.controller.show_frame("Home")
        
    def change_theme(self, theme):
        if theme == "Dark":
            ctk.set_appearance_mode("dark")
            self.appconfig.update_color("white")
        else:
            ctk.set_appearance_mode("light")
            self.appconfig.update_color("black")
            
        
    def save_settings(self):
        self.change_theme(self.theme_var.get())
        self.appconfig.update_font(self.font_var.get())
        self.appconfig.update_color(self.font_color_var.get())
        self.controller.refresh_app()
