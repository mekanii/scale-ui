import tkinter as tk

class ScaleContent:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg='white')
        self.frame.pack(pady=10, fill=tk.X)

        # Create and configure content label
        self.content_label = tk.Label(self.frame, text="Scale", font=("Segoe UI", 24), anchor='w', bg='white')
        self.content_label.pack(pady=10, anchor='w')