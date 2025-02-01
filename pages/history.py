import customtkinter as ctk
import sqlite3  # For SQLite database
from datetime import datetime

from .constants import AppConfig  # Importing AppConfig, though it's not used in this snippet
from .frame_helper import FrameHelper  # Importing FrameHelper for additional functionalities


class History(ctk.CTkFrame, FrameHelper):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        FrameHelper.__init__(self)

        self.controller = controller
        self.item_count = 0  # Counter for tracking the number of items

        self.initialize_ui()

    def initialize_ui(self):
        """Initializes the UI components."""
        # Create a canvas widget for scrolling
        self.canvas = ctk.CTkCanvas(self)
        self.canvas.pack(side="left", fill="both", expand=True)

        # Create a vertical scrollbar for the canvas
        self.scrollbar = ctk.CTkScrollbar(
            self, orientation="vertical", command=self.canvas.yview
        )
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Create a frame to hold all your widgets
        self.scrollable_frame = ctk.CTkFrame(self.canvas)

        # Create a window in the canvas to contain the scrollable frame
        self.canvas.create_window((200, 0), window=self.scrollable_frame, anchor="nw")
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        # Back button
        back_button = ctk.CTkButton(
            self.scrollable_frame, text="Back", command=self.go_to_home
        )
        back_button.grid(row=0, column=0, padx=10, pady=10)

        # Load items from the database
        self.load_items_from_db()

    def load_items_from_db(self):
        """Fetches and displays items from the database."""
        try:
            # Connect to the database
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()

            # Query to fetch items
            cursor.execute("SELECT id, item_name, timestamp FROM history_items")
            rows = cursor.fetchall()

            # Add each row to the scrollable frame
            for row in rows:
                _, item_name, item_date = row
                self.add_item_to_frame(item_name, item_date)

            conn.close()

        except sqlite3.Error as e:
            print(f"Database error: {e}")

    def add_item_to_frame(self, item_name, date):
        """Add an item with a count and the provided date."""
        self.item_count += 1  # Increment item count

        # Format the date parameter (ensure it's a string)
        if isinstance(date, datetime):
            date_str = date.strftime("%Y-%m-%d %H:%M:%S")
        else:
            date_str = str(date)  # In case the date is already in string format

        # Create the label for the new item
        item_label = f"Item {self.item_count}:\n{item_name}\n Added on {date_str}"

        new_item = ctk.CTkLabel(
            self.scrollable_frame,
            text=item_label,
            font=("Arial", 14),
            fg_color="white",  # Set background color
            text_color="black",  # Set text color
            corner_radius=10,  # Round corners for a softer look
        )

        # Place the item in the grid with a dynamic row height and padding
        new_item.grid(row=self.item_count, column=0, padx=20, pady=15, sticky="w")

    def go_to_home(self):
        """Navigate back to the home frame."""
        self.controller.show_frame("Home")
