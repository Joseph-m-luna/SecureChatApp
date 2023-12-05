import tkinter as tk
from tkinter import Canvas, Scrollbar, Entry, Button, Label, LEFT, RIGHT, END, RAISED
from datetime import datetime

class ChatApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Application")
        self.root.geometry("600x400")  # Set the initial window size

        # Create a Canvas for messages with a Scrollbar
        self.canvas = Canvas(root)
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollbar = Scrollbar(root, command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Create a frame to hold messages
        self.messages_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.messages_frame, anchor="nw")

        # Create Entry widget for typing messages
        self.entry_frame = tk.Frame(root)
        self.entry_frame.pack(side="bottom", fill="both", pady=5)
        self.entry_field = Entry(self.entry_frame)
        self.entry_field.pack(side="left", fill="both", expand=True)

        # Create Send button
        self.send_button = Button(self.entry_frame, text="Send", command=self.send_message)
        self.send_button.pack(side="right")

        # Bind Enter key to send_message function
        self.entry_field.bind("<Return>", lambda event: self.send_message())

    def send_message(self):
        message = self.entry_field.get()
        if message:
            # Get current timestamp for metadata
            timestamp = datetime.now().strftime("%H:%M")

            # Create a frame for the message components with a border
            message_frame = tk.Frame(self.messages_frame, padx=10, pady=5, bd=2, relief=RAISED)
            message_frame.pack(anchor="w", pady=5, padx=10, fill="both")

            # Create a label for the username header
            username_label = Label(message_frame, text="Username", font=("Helvetica", 10, "bold"))
            username_label.pack(anchor="w")

            # Create a label for the message text
            message_label = Label(message_frame, text=message, justify=LEFT)
            message_label.pack(anchor="w")

            # Create a label for the metadata
            metadata_label = Label(message_frame, text=f"{timestamp} - Read", font=("Helvetica", 8))
            metadata_label.pack(anchor="w", pady=(5, 0))

            # Update the Canvas to accommodate new messages
            self.canvas.update_idletasks()
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))

            # Clear the entry field
            self.entry_field.delete(0, "end")

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApplication(root)
    root.mainloop()