import tkinter as tk
from tkinter import simpledialog, messagebox, PhotoImage
from include.button_hover import on_enter, on_leave
from include.frame_hover import frame_selected, frame_enter, frame_leave
import requests
import os
import json

class CalibrationContent:
    def __init__(self, parent):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        icon_dir = os.path.join(current_dir, "assets", "icons")

        self.frame = tk.Frame(parent, bg='white')
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)

        l_frame = tk.Frame(self.frame, bg='white')
        l_frame.grid(row=0, padx=(0, 10), pady=10, column=0, sticky='nsew')
        r_frame = tk.Frame(self.frame, bg='white')
        r_frame.grid(row=0, pady=10, column=1, sticky='nsew')

        # Create and configure content label
        self.content_label = tk.Label(l_frame, text="Calibration Setting", font=("Segoe UI", 24), anchor='w', bg='white')
        self.content_label.pack(pady=10, anchor='w')