from .app import App
from .login import Login
from .home import Home

# Pages for the application for ease of use
pages = {
    "Login": Login,
    "Home": Home
}

def start_app():
    """
    Initializes and starts the app by passing the pages dictionary to the App class
    and running the main application loop.
    """
    app = App(pages)
    app.mainloop()

if __name__ == "__main__":
    start_app()
