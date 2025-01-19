import customtkinter as ctk
from tkinter import StringVar, IntVar

from .constants import AppConfig
from .frame_helper import FrameHelper


class History(ctk.CTkFrame, FrameHelper):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)

        self.controller = controller
        self.initialize_ui()

    def initialize_ui(self):
        # Create a canvas widget for scrolling
        
        self.canvas = ctk.CTkCanvas(self)
        self.canvas.pack(side="left", fill="both", expand=True)

        # Create a vertical scrollbar for the canvas
        self.scrollbar = ctk.CTkScrollbar(
            self, orientation="vertical", command=self.canvas.yview
        )
        self.scrollbar.pack(side="right", fill="y")

        # Create a frame to hold all your widgets
        self.scrollable_frame = ctk.CTkFrame(self.canvas)

        # Create a window in the canvas to contain the scrollable frame
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        label = ctk.CTkButton(self.scrollable_frame, text="Back", command=self.go_to_home)
        label.grid(row=0, column=0, padx=10, pady=10)

    

    def toggle_scrollbar(self):
        if self.scrollbar_var.get():
            print("Scrollbar enabled.")
        else:
            print("Scrollbar disabled.")

    def go_to_home(self):
        self.controller.show_frame("Home")

    