import tkinter as tk
from tkinter import simpledialog, messagebox, PhotoImage
from include.button_hover import on_enter, on_leave
from include.frame_hover import frame_selected, frame_enter, frame_leave
import requests
import os
import json

class StandardContent:
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

        self.content_label = tk.Label(l_frame, text="Standard", font=("Segoe UI", 24), anchor='w', bg='white', fg='black')
        self.content_label.pack(pady=10, anchor='w')

        self.reload_icon = PhotoImage(file=os.path.join(icon_dir, "refresh-solid-36.png"))
        self.reload_button = tk.Button(
            l_frame,
            padx=10,
            pady=10,
            anchor='w',
            justify='left',
            image=self.reload_icon,
            compound=tk.LEFT,
            text="Reload",
            bg='white',
            relief=tk.FLAT,
            font=('Segoe UI', 10),
            command=self.load_data,
            fg='black'
        )
        self.reload_button.pack(pady=5, fill=tk.X)
        self.reload_button.bind("<Enter>", lambda e: on_enter(e, color='#f1f2f3'))
        self.reload_button.bind("<Leave>", lambda e: on_leave(e, color='white'))

        self.list_frame = tk.Frame(l_frame, bg='white')
        self.list_frame.pack(fill=tk.X)

        self.load_data()

    def load_data(self):
        try:
            with open('config.json', 'r') as file:
                json_data = json.load(file)
                base_api_url = json_data.get('default', None)
                response = requests.get(f"http://{base_api_url}/standards")
                response.raise_for_status()
                response_json = response.json()
                data = response_json.get('data', [])

                for widget in self.list_frame.winfo_children():
                    widget.destroy()

                item_count_label = tk.Label(
                    self.list_frame,
                    text=str(len(data))+' standards found',
                    font=('Segoe UI', 14),
                    bg='white',
                    anchor='w',
                    fg='black'
                )
                item_count_label.pack(pady=(20, 5), fill=tk.X)

                for standard in data:
                    item_frame = tk.Frame(self.list_frame, bg='white')
                    item_frame.pack(fill=tk.X)
                    data_label = tk.Label(
                        item_frame,
                        padx=10,
                        pady=10,
                        text=standard['name'],
                        font=('Segoe UI', 10),
                        bg='white',
                        anchor='w',
                        fg='black'
                    )
                    data_label.pack(fill=tk.X)
                    data_label.bind('<Enter>', frame_enter)
                    data_label.bind('<Leave>', frame_leave)
                    data_label.bind('<Button-1>', frame_selected)

        except requests.RequestException as e:
            messagebox.showerror("Error", f"Failed to load data: {e}")