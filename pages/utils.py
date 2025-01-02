import customtkinter as ctk
from customtkinter import filedialog


def create_popup_entry() -> str:
    popup = ctk.CTkToplevel()
    popup.title("Enter your code")
    popup.geometry("300x200")

    user_input_val = ctk.StringVar()

    label = ctk.CTkLabel(popup, text="Please enter verification code from Apple:")
    label.pack(padx=10, pady=10)

    entry = ctk.CTkEntry(
        popup, placeholder_text="Enter Code", textvariable=user_input_val
    )
    entry.pack(padx=10, pady=10)

    def submit():
        popup.destroy()

    submit_button = ctk.CTkButton(popup, text="Submit", command=submit)
    submit_button.pack(pady=10)

    popup.wait_window()

    return user_input_val.get()

def select_file():
    folder_path = filedialog.askdirectory(title="Select Folder")
    if folder_path:
        return folder_path
    return None

