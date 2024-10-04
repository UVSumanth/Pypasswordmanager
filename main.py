from cryptography.fernet import Fernet
import json
import os
import tkinter as tk
from tkinter import messagebox, simpledialog

# Color Scheme
PRIMARY_COLOR = "#3498db"  # Blue
SECONDARY_COLOR = "#2ecc71"  # Green
ACCENT_COLOR = "#e74c3c"  # Red
BACKGROUND_COLOR = "#ecf0f1"  # Light Gray
TEXT_COLOR = "#2c3e50"  # Dark Gray


# Generate a key for encryption
def generate_key():
    return Fernet.generate_key()


# Save passwords to a file
def save_passwords(passwords):
    with open('passwords.json', 'w') as f:
        json.dump(passwords, f)


# Load passwords from a file
def load_passwords():
    if os.path.exists('passwords.json'):
        with open('passwords.json', 'r') as f:
            return json.load(f)
    return {}


class PasswordManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Password Manager")
        self.root.configure(bg=BACKGROUND_COLOR)

        # Generate a key for encryption
        self.key = generate_key()
        self.cipher = Fernet(self.key)
        self.passwords = load_passwords()

        # Create GUI elements
        self.create_widgets()

    def create_widgets(self):
        # Title Label
        title_label = tk.Label(self.root, text="Password Manager", font=("Arial", 16), bg=BACKGROUND_COLOR,
                               fg=TEXT_COLOR)
        title_label.pack(pady=10)

        # Button Frame
        button_frame = tk.Frame(self.root, bg=BACKGROUND_COLOR)
        button_frame.pack(pady=10)

        # Add Password Button
        self.add_button = tk.Button(button_frame, text="Add Password", command=self.add_password, bg=PRIMARY_COLOR,
                                    fg="white")
        self.add_button.grid(row=0, column=0, padx=5)

        # Retrieve Password Button
        self.retrieve_button = tk.Button(button_frame, text="Retrieve Password", command=self.retrieve_password,
                                         bg=SECONDARY_COLOR, fg="white")
        self.retrieve_button.grid(row=0, column=1, padx=5)

        # Delete Password Button
        self.delete_button = tk.Button(button_frame, text="Delete Password", command=self.delete_password,
                                       bg=ACCENT_COLOR, fg="white")
        self.delete_button.grid(row=0, column=2, padx=5)

        # Exit Button
        self.exit_button = tk.Button(self.root, text="Exit", command=self.root.quit, bg=ACCENT_COLOR, fg="white")
        self.exit_button.pack(pady=20)

        # Status Label
        self.status_label = tk.Label(self.root, text="", bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
        self.status_label.pack(pady=10)

    def add_password(self):
        username = simpledialog.askstring("Input", "Enter username:", parent=self.root)
        password = simpledialog.askstring("Input", "Enter password:", show='*', parent=self.root)

        if username and password:
            encrypted_password = self.cipher.encrypt(password.encode()).decode()
            self.passwords[username] = encrypted_password
            save_passwords(self.passwords)
            self.update_status(f"Password for '{username}' saved!")

    def retrieve_password(self):
        username = simpledialog.askstring("Input", "Enter username to retrieve password:", parent=self.root)

        if username in self.passwords:
            decrypted_password = self.cipher.decrypt(self.passwords[username].encode()).decode()
            messagebox.showinfo("Password", f"Password for '{username}': {decrypted_password}", parent=self.root)
        else:
            self.update_status("Username not found!")

    def delete_password(self):
        username = simpledialog.askstring("Input", "Enter username to delete password:", parent=self.root)

        if username in self.passwords:
            del self.passwords[username]
            save_passwords(self.passwords)
            self.update_status(f"Password for '{username}' deleted!")
        else:
            self.update_status("Username not found!")

    def update_status(self, message):
        self.status_label.config(text=message)


if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordManagerApp(root)
    root.mainloop()
