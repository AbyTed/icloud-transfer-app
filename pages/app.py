import customtkinter as ctk


class App(ctk.CTk):
    """
    A custom Tkinter application class that manages multiple pages and provides a container for them.
    Attributes:
        frames (dict): A dictionary to store the frames (pages) of the application.
        pages (dict): A dictionary containing the page names and their corresponding classes.
        bot (None): Placeholder for a bot instance (if any).
    Methods:
        __init__(pages, *args, **kwargs):
            Initializes the application, sets the theme, creates the container frame, and initializes the pages.
        show_frame(cont):
            Raises the specified frame to the top, making it visible.
        refresh_app():
            Refreshes the UI of all frames to apply updated styles.
    """
    def __init__(self, pages, *args, **kwargs):
        ctk.CTk.__init__(self, *args, **kwargs)
        
        # Set the theme
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("dark-blue")
        
        # Create a container frame
        container = ctk.CTkFrame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Initialize frames to an empty dictionary
        self.frames = {}
        self.pages = pages
        self.bot = None
        self.title("Icloud Bot Transfer")
        
        # Iterate through the pages dictionary and create frames
        for page_name, page in pages.items():
            try:
                frame = page(container, self)
                self.frames[page_name] = frame
                frame.grid(row=0, column=0, sticky="nsew")
            except Exception as e:
                print(f"Error: {e}")

        # Show the initial frame
        self.show_frame("Login")

    def show_frame(self, cont):
        """Raise the specified frame to the top."""
        frame = self.frames[cont]
        frame.tkraise()

    def refresh_app(self):
        """Refresh the UI of all frames to apply updated styles."""
        for frame in self.frames.values():
            if hasattr(frame, "refresh_ui"):
                frame.refresh_ui()
