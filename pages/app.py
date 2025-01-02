import customtkinter as ctk

from .constants import COLOR_BACKGROUND

class App(ctk.CTk):
    def __init__(self, pages, *args, **kwargs):
        ctk.CTk.__init__(self, *args, **kwargs)
        #theme
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("dark-blue")
        
        # creating a container
        container = ctk.CTkFrame(self)
        container.pack(side="top", fill="both", expand=True)
        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # initializing frames to an empty dictionary
        self.frames = {}
        self.pages = pages
        self.bot = None
        
        # iterating through a tuple consisting
        # of the different page layouts
        for page_name, page in pages.items():
            try:
                frame = page(container, self)
                
                self.frames[page_name] = frame
                
                frame.grid(row=0, column=0, sticky="nsew")
                
            except Exception as e:
                print(f'error {e}')
        
        
        
        self.show_frame("Login")

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()