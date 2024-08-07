import tkinter as tk

class AboutContent:
    def __init__(self, parent, tasks):
        self.tasks = tasks
        
        self.frame = tk.Frame(parent, bg='white')
        self.frame.pack(pady=10, fill=tk.X)

        # Create and configure content label
        self.content_label = tk.Label(self.frame, text="About Us", font=("Segoe UI", 24), anchor='w', bg='white', fg='black')
        self.content_label.pack(pady=10, anchor='w')