import sqlite3
import os


class FrameHelper:
    def __init__(self):
        # Set the path to the SQLite database
        self.database_path = os.path.join(
            os.path.dirname(__file__), "../data/history.db"
        )
        # Ensure the database exists or create a new one
        self.ensure_database()

    def ensure_database(self):
        """Ensure the database starts with a blank piece of data."""
        if os.path.exists(self.database_path):
            print("Database already exists.")
        else:
            print("Creating a new blank database...")
            self.create_history_table()

    def get_connection(self):
        """Create and return a connection to the database."""
        try:
            return sqlite3.connect(self.database_path)
        except sqlite3.Error as e:
            print(f"Error connecting to the database: {e}")
            return None

    def initialize_ui(self):
        """Placeholder method for initializing the UI."""
        print("define your own initialize_ui for using tkinter or customertkinter")

    def refresh_ui(self):
        """Refresh UI elements based on updated constants."""
        for widget in self.winfo_children():
            widget.destroy()  # Clear current widgets
        self.initialize_ui()  # Reinitialize with updated styles

    def add_item_to_db(self, item_name):
        """Add a new item to the history_items table in the database."""
        try:
            self.database_path = os.path.join(
                os.path.dirname(__file__), "../data/history.db"
            )
            # Connect to the database
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()

            # Insert the item into the table
            cursor.execute("INSERT INTO history_items (item_name) VALUES (?)", (item_name,))

            # Commit the changes and close the connection
            conn.commit()
            conn.close()

            print(f"Item '{item_name}' added to database.")
        except sqlite3.Error as e:
            print(f"Error adding item to database: {e}")

    def create_history_table(self):
        """Create the history_items table if it does not exist."""
        conn = self.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    CREATE TABLE history_items (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        item_name TEXT NOT NULL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                """
                )
                conn.commit()
                print("History table ensured.")
            except sqlite3.Error as e:
                print(f"Error creating table: {e}")
            finally:
                conn.close()
