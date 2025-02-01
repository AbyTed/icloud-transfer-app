import json
import os


class AppConfig:
    """
    A class used to manage the application configuration settings.
    Attributes
    ----------
    CONFIG_FILE : str
        The path to the JSON configuration file.
    _settings_cache : dict or None
        Internal cache for loaded settings.
    Methods
    -------
    __init__()
        Initializes the AppConfig instance and loads settings from the JSON file.
    _load_config()
        Loads the JSON configuration from the file.
    _save_config(config_data)
        Saves the JSON configuration to the file.
    _get_settings()
        Returns the settings, reloading if necessary.
    _reload_settings()
        Forces reloading of the settings from the JSON file.
    save_threading(threading)
        Toggles the threading value and saves it.
    update_font(font_name, size=None, style=None)
        Updates font settings and saves them to the JSON file.
    update_color(color_value, color_key="COLOR_TEXT")
        Updates color settings and saves them to the JSON file.
    update_widget_style(style_key, style_value)
        Updates widget style settings and saves them to the JSON file.
    """
    CONFIG_FILE = "pages/settings.json"

    # Internal cache for loaded settings
    _settings_cache = None

    def __init__(self):
        """Initializes the AppConfig instance and loads settings from the JSON file."""
        self._settings_cache = self._load_config()
        # Load font settings
        self.LARGE_FONT = tuple(self._settings_cache["fonts"]["LARGE_FONT"])
        self.FONT_PRIMARY = tuple(self._settings_cache["fonts"]["FONT_PRIMARY"])
        self.FONT_SECONDARY = tuple(self._settings_cache["fonts"]["FONT_SECONDARY"])
        self.FONT_TITLE = tuple(self._settings_cache["fonts"]["FONT_TITLE"])

        # Load color settings
        self.COLOR_PRIMARY = self._settings_cache["colors"]["COLOR_PRIMARY"]
        self.COLOR_SECONDARY = self._settings_cache["colors"]["COLOR_SECONDARY"]
        self.COLOR_ACCENT = self._settings_cache["colors"]["COLOR_ACCENT"]
        self.COLOR_TEXT = self._settings_cache["colors"]["COLOR_TEXT"]
        self.COLOR_TEXT_SECONDARY = self._settings_cache["colors"]["COLOR_TEXT_SECONDARY"]
        self.COLOR_BACKGROUND = self._settings_cache["colors"]["COLOR_BACKGROUND"]
        self.COLOR_HIGHLIGHT = self._settings_cache["colors"]["COLOR_HIGHLIGHT"]
        self.COLOR_ERROR = self._settings_cache["colors"]["COLOR_ERROR"]

        # Load widget style settings
        self.BUTTON_COLOR = self._settings_cache["widget_styles"]["BUTTON_COLOR"]
        self.BUTTON_HOVER = self._settings_cache["widget_styles"]["BUTTON_HOVER"]
        self.ENTRY_COLOR = self._settings_cache["widget_styles"]["ENTRY_COLOR"]
        self.ENTRY_TEXT_COLOR = self._settings_cache["widget_styles"]["ENTRY_TEXT_COLOR"]
        self.SCROLLBAR_COLOR = self._settings_cache["widget_styles"]["SCROLLBAR_COLOR"]
        self.SCROLLBAR_HOVER = self._settings_cache["widget_styles"]["SCROLLBAR_HOVER"]

        # Load threading setting
        self.THREADING = self._settings_cache["threading"]

    def _load_config(self):
        """Loads the JSON configuration from the file."""
        if not os.path.exists(self.CONFIG_FILE):
            return {}
        with open(self.CONFIG_FILE, "r") as file:
            return json.load(file)

    def _save_config(self, config_data):
        """Saves the JSON configuration to the file."""
        with open(self.CONFIG_FILE, "w") as file:
            json.dump(config_data, file, indent=4)

    def _get_settings(self):
        """Returns the settings, reloading if necessary."""
        if self._settings_cache is None:
            self._settings_cache = self._load_config()
        return self._settings_cache

    def _reload_settings(self):
        """Forces reloading of the settings from the JSON file."""
        self._settings_cache = self._load_config()

    def save_threading(self, threading):
        """Toggles the threading value and saves it."""
        config_data = self._get_settings()
        config_data["threading"] = threading
        self._save_config(config_data)
        self._reload_settings()

    def update_font(self, font_name, size=None, style=None):
        """Updates font settings and saves them to the JSON file."""
        config_data = self._get_settings()

        if "fonts" not in config_data:
            config_data["fonts"] = {}

        # Update primary and secondary fonts
        config_data["fonts"]["FONT_PRIMARY"] = (
            font_name,
            (
                size
                if size is not None
                else config_data["fonts"].get("FONT_PRIMARY", [font_name, 14])[1]
            ),
        )
        config_data["fonts"]["FONT_SECONDARY"] = (
            font_name,
            (
                size
                if size is not None
                else config_data["fonts"].get("FONT_SECONDARY", [font_name, 12])[1]
            ),
        )

        # Update title font with optional style
        if style is not None:
            config_data["fonts"]["FONT_TITLE"] = (
                font_name,
                (
                    size
                    if size is not None
                    else config_data["fonts"].get("FONT_TITLE", [font_name, 18])[1]
                ),
                style,
            )
        else:
            config_data["fonts"]["FONT_TITLE"] = (
                font_name,
                (
                    size
                    if size is not None
                    else config_data["fonts"].get("FONT_TITLE", [font_name, 18])[1]
                ),
                config_data["fonts"].get("FONT_TITLE", ["Helvetica", 18, "bold"])[2],
            )

        self._save_config(config_data)
        self._reload_settings()

    def update_color(self, color_value, color_key="COLOR_TEXT"):
        """Updates color settings and saves them to the JSON file."""
        config_data = self._get_settings()

        if "colors" not in config_data:
            config_data["colors"] = {}

        config_data["colors"][color_key] = color_value

        self._save_config(config_data)
        self._reload_settings()

    def update_widget_style(self, style_key, style_value):
        """Updates widget style settings and saves them to the JSON file."""
        config_data = self._get_settings()

        if "widget_styles" not in config_data:
            config_data["widget_styles"] = {}

        config_data["widget_styles"][style_key] = style_value

        self._save_config(config_data)
        self._reload_settings()
