class FrameHelper():
    def initialize_ui(self):
        print('define your own initialize_ui for using tkinter or customertkinter')
    
    def refresh_ui(self):
        """Refresh UI elements based on updated constants."""
        for widget in self.winfo_children():
            widget.destroy()  # Clear current widgets
        self.initialize_ui()  # Reinitialize with updated styles