import tkinter as tk
from tkinter import scrolledtext, messagebox

class MessagingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Messaging App")
        self.root.geometry("600x600")
        self.root.configure(bg="#f0f0f0")

        # List of users
        self.users = ["User 1", "User 2", "User 3"]
        self.current_user = "User 1"
        self.messages = {user: [] for user in self.users}  # Store messages for each user
        self.favorites = {user: [] for user in self.users}  # Store favorite messages for each user

        # User selection
        self.user_label = tk.Label(self.root, text="Select User:", font=("Arial", 12), bg="#f0f0f0")
        self.user_label.pack(pady=5)
        self.user_dropdown = tk.StringVar(value=self.current_user)
        self.user_menu = tk.OptionMenu(self.root, self.user_dropdown, *self.users, command=self.switch_user)
        self.user_menu.pack(pady=5)

        # Chat display
        self.chat_display = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, state="disabled", bg="#ffffff", font=("Arial", 12))
        self.chat_display.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Message entry
        self.message_entry = tk.Entry(self.root, font=("Arial", 14), bg="#ffffff")
        self.message_entry.pack(pady=5, padx=10, fill=tk.X)
        self.message_entry.bind("<Return>", self.send_message)

        # Buttons
        self.send_button = tk.Button(self.root, text="Send", command=self.send_message, bg="#4caf50", fg="white", font=("Arial", 12))
        self.send_button.pack(pady=5)

        self.favorite_button = tk.Button(self.root, text="Mark/Unmark as Favorite", command=self.mark_favorite, bg="#ff9800", fg="white", font=("Arial", 12))
        self.favorite_button.pack(pady=5)

        self.view_favorites_button = tk.Button(self.root, text="View Favorites", command=self.view_favorites, bg="#2196f3", fg="white", font=("Arial", 12))
        self.view_favorites_button.pack(pady=5)

    def switch_user(self, selected_user):
        """Switch the current user and display their chat."""
        self.current_user = selected_user
        self.refresh_chat()

    def send_message(self, event=None):
        """Send a message to the current user's chat."""
        message = self.message_entry.get().strip()
        if message:
            self.messages[self.current_user].append({"message": message, "favorite": False})
            self.message_entry.delete(0, tk.END)
            self.refresh_chat()
        else:
            messagebox.showwarning("Warning", "Message cannot be empty!")

    def refresh_chat(self):
        """Refresh the chat display with messages for the current user."""
        self.chat_display.config(state="normal")
        self.chat_display.delete(1.0, tk.END)
        for index, msg in enumerate(self.messages[self.current_user]):
            favorite_symbol = "★" if msg["favorite"] else " "
            display_msg = f"{index + 1}. [{favorite_symbol}]: {msg['message']}\n"
            self.chat_display.insert(tk.END, display_msg)
        self.chat_display.config(state="disabled")

    def mark_favorite(self):
        """Mark/unmark a specific message as favorite."""
        index = self.get_message_index()
        if index is not None:
            self.messages[self.current_user][index]["favorite"] = not self.messages[self.current_user][index]["favorite"]
            self.refresh_chat()

    def view_favorites(self):
        """Show a list of favorite messages for the current user."""
        favorites = [msg["message"] for msg in self.messages[self.current_user] if msg["favorite"]]
        if favorites:
            messagebox.showinfo("Favorites", "\n".join(favorites))
        else:
            messagebox.showinfo("Favorites", "No favorite messages yet!")

    def get_message_index(self):
        """Prompt the user to select a message by its index."""
        try:
            index = int(self.message_entry.get().strip()) - 1
            if 0 <= index < len(self.messages[self.current_user]):
                return index
            else:
                messagebox.showwarning("Invalid Index", "Please enter a valid message number.")
        except ValueError:
            messagebox.showwarning("Invalid Input", "Please enter a valid number.")
        return None


if __name__ == "__main__":
    root = tk.Tk()
    app = MessagingApp(root)
    root.mainloop()
