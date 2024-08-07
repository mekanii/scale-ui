import sys
import os

# Ensure standard library paths are prioritized
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'module')))

import tkinter as tk
from tkinter import simpledialog, messagebox, PhotoImage
from include.button_hover import on_enter, on_leave
from include.frame_hover import frame_selected, frame_enter, frame_leave
import requests
import json
import asyncio
import threading
import pygame

def start_event_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

class ScaleContent:
    def __init__(self, parent, tasks):
        pygame.mixer.init()

        self.last_check = None
        self.continuous_reading = False
        self.tasks = tasks

        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.icon_dir = os.path.join(current_dir, "assets", "icons")

        self.frame = tk.Frame(parent, bg='white')
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)

        l_frame = tk.Frame(self.frame, bg='white')
        l_frame.grid(row=0, padx=(0, 10), pady=10, column=0, sticky='nsew')
        r_frame = tk.Frame(self.frame, bg='white')
        r_frame.grid(row=0, pady=10, column=1, sticky='nsew')

        self.content_label = tk.Label(l_frame, text="Scale", font=("Segoe UI", 24), anchor='w', bg='white', fg='black')
        self.content_label.pack(pady=10, anchor='w')

        self.reload_icon = PhotoImage(file=os.path.join(self.icon_dir, "refresh-solid-36.png"))
        self.reload_button = tk.Button(
            l_frame,
            padx=10,
            anchor='w',
            justify='left',
            image=self.reload_icon,
            compound=tk.LEFT,
            text="Reload",
            bg='white',
            relief=tk.FLAT,
            font=('Segoe UI', 10),
            command=lambda: self.tasks.append(asyncio.run_coroutine_threadsafe(self.load_data(), self.loop)),
            fg='black',
            bd=0,
            borderwidth=0,
            highlightthickness=0
        )
        self.reload_button.pack(pady=5, ipady=10, fill=tk.X)
        self.reload_button.bind("<Enter>", lambda e: on_enter(e, color='#f1f2f3'))
        self.reload_button.bind("<Leave>", lambda e: on_leave(e, color='white'))

        self.list_frame = tk.Frame(l_frame, bg='white')
        self.list_frame.pack(fill=tk.X)

        self.loop = asyncio.new_event_loop()
        threading.Thread(target=start_event_loop, args=(self.loop,), daemon=True).start()
        self.tasks.append(asyncio.run_coroutine_threadsafe(self.load_data(), self.loop))

    async def load_data(self):
        try:
            with open('config.json', 'r') as file:
                self.reload_button.config(state='disabled')
                json_data = json.load(file)
                base_api_url = json_data.get('default', None)
                response = await asyncio.to_thread(requests.get, f"http://{base_api_url}/parts")
                response.raise_for_status()
                response_json = response.json()
                data = response_json.get('data', [])

                for widget in self.list_frame.winfo_children():
                    widget.destroy()

                item_count_label = tk.Label(
                    self.list_frame,
                    text=str(len(data))+' part standards found',
                    font=('Segoe UI', 14),
                    bg='white',
                    anchor='w',
                    fg='black'
                )
                item_count_label.pack(pady=(20, 5), fill=tk.X)

                self.dropdown = tk.StringVar()
                self.dropdown.set("Select part standard")
                options = [row['name'] for row in data]
                self.dropdown_menu = tk.OptionMenu(
                    self.list_frame,
                    self.dropdown,
                    *options
                )
                self.dropdown_menu.config(
                    padx=10,
                    pady=10,
                    bg='white',
                    font=('Segoe UI', 10),
                    relief=tk.FLAT,
                    anchor='w',
                    justify='left',
                    fg='black'
                )
                self.dropdown_menu.pack(fill=tk.X)

                self.connect_icon = PhotoImage(file=os.path.join(self.icon_dir, "refresh-solid-36.png"))
                self.connect_button = tk.Button(
                    self.list_frame,
                    padx=10,
                    anchor='w',
                    justify='left',
                    image=self.connect_icon,
                    compound=tk.LEFT,
                    text="Connect",
                    bg='white',
                    relief=tk.FLAT,
                    font=('Segoe UI', 10),
                    command=lambda: self.tasks.append(asyncio.run_coroutine_threadsafe(self.start(self.dropdown.get(), data) if self.connect_button['text'] == 'Connect' else self.stop(), self.loop)),
                    fg='black',
                    bd=0,
                    borderwidth=0,
                    highlightthickness=0
                )
                self.connect_button.pack(pady=5, ipady=10, fill=tk.X)

                self.tare_icon = PhotoImage(file=os.path.join(self.icon_dir, "refresh-solid-36.png"))
                self.tare_button = tk.Button(
                    self.list_frame,
                    padx=10,
                    anchor='w',
                    justify='left',
                    image=self.connect_icon,
                    compound=tk.LEFT,
                    text="Tare",
                    bg='white',
                    relief=tk.FLAT,
                    font=('Segoe UI', 10),
                    command=lambda: self.tasks.append(asyncio.run_coroutine_threadsafe(self.tare(), self.loop)),
                    fg='black',
                    bd=0,
                    borderwidth=0,
                    highlightthickness=0
                )
                self.tare_button.pack(pady=5, ipady=10, fill=tk.X)

                self.connect_button.bind("<Enter>", lambda e: on_enter(e, color='#f1f2f3'))
                self.connect_button.bind("<Leave>", lambda e: on_leave(e, color='white'))
                self.tare_button.bind("<Enter>", lambda e: on_enter(e, color='#f1f2f3'))
                self.tare_button.bind("<Leave>", lambda e: on_leave(e, color='white'))

                self.indicator_label = tk.Label(
                    self.list_frame,
                    text="",
                    font=('Segoe UI', 48),
                    bg='white',
                    anchor='e',
                    justify='right',
                    fg='black'
                )
                self.indicator_label.pack(pady=(20, 5), fill=tk.X)

                self.status_label = tk.Label(
                    self.list_frame,
                    text="",
                    font=('Segoe UI', 32),
                    bg='white',
                    anchor='w',
                    justify='left',
                    fg='black'
                )
                self.status_label.pack(fill=tk.X)

                self.reload_button.config(state='normal')
                self.tare_button.config(state='disabled')

        except requests.RequestException as e:
            messagebox.showerror("Error", f"Failed to load data: {e}")

    def enable_buttons(self):
        self.reload_button.config(state='normal')

    def disable_buttons(self):
        self.reload_button.config(state='disabled')

    async def start(self, part_name, data):
        self.tare_button.config(state='normal')
        self.continuous_reading = True
        for part in data:
            if part['name'] == part_name:
                self.connect_button.config(text="Disconnect")
                try:
                    with open('config.json', 'r') as file:
                        json_data = json.load(file)
                        base_api_url = json_data.get('default', None)
                        while self.connect_button['text'] == "Disconnect":
                            if self.continuous_reading:
                                response = await asyncio.to_thread(requests.post, f"http://{base_api_url}/scale?std={part['std']}&unit={part['unit']}")
                                response.raise_for_status()
                                response_json = response.json()
                                data = response_json.get('data', {})
                                if part['unit'] == 'kg':
                                    weight = f"{max(0, float(format(data['weight'], '.2f')))} {part['unit']}"
                                else:
                                    weight = f"{max(0, int(data['weight']))} {part['unit']}"
                                if data['check'] == 1 and data['check'] != self.last_check:
                                    print(data)
                                    self.tasks.append(asyncio.run_coroutine_threadsafe(self.play_tone("OK"), self.loop))
                                    self.status_label.config(fg='green')
                                    self.status_label.config(text="QTY GOOD")
                                elif data['check'] == 2 and data['check'] != self.last_check:
                                    print(data)
                                    self.tasks.append(asyncio.run_coroutine_threadsafe(self.play_tone("NG"), self.loop))
                                    self.status_label.config(fg='red')
                                    self.status_label.config(text="NOT GOOD")
                                elif data['check'] == 0 and data['check'] != self.last_check:
                                    self.status_label.config(text="")
                                self.last_check = data['check']
                                self.indicator_label.config(text=weight)
                            else:
                                await asyncio.sleep(0.1)
                except requests.RequestException as e:
                    messagebox.showerror("Error", f"Failed to load data: {e}")
                    self.connect_button.config(text="Disconnect")
                    self.continuous_reading = False
                    self.tare_button.config(state='disabled')

    async def stop(self):
        self.connect_button.config(text="Connect")
        self.tare_button.config(state='disabled')
        self.continuous_reading = False

    async def tare(self):
        try:
            with open('config.json', 'r') as file:
                self.tare_button.config(state='disabled')
                self.connect_button.config(state='disabled')
                self.reload_button.config(state='disabled')

                last_continuous_reading = self.continuous_reading
                if self.continuous_reading:
                    self.continuous_reading = False
                json_data = json.load(file)
                base_api_url = json_data.get('default', None)
                response = await asyncio.to_thread(requests.get, f"http://{base_api_url}/tare")
                response.raise_for_status()
                response_json = response.json()
                data = response_json.get('data', {})

                self.connect_button.config(state='normal')
                self.tare_button.config(state='normal')
                self.reload_button.config(state='normal')
                self.continuous_reading = last_continuous_reading
        except requests.RequestException as e:
            messagebox.showerror("Error", f"Failed to load data: {e}")
            self.connect_button.config(text="Disconnect")

    async def play_tone(self, status):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        filename = ""
        if status == "OK":
            filename = "OK.mp3"
        elif status == "NG":
            filename = "NG.mp3"
        sound_path = os.path.join(current_dir, "assets", "tone", filename)
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.play()