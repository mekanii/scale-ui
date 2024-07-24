import tkinter as tk
from tkinter import PhotoImage
from include.button_hover import on_enter, on_leave
import os

class Sidebar:
    def __init__(self, master, show_scale, show_standard, show_calibration, show_devices, show_about):
        self.master = master
        self.show_scale = show_scale
        self.show_standard = show_standard
        self.show_calibration = show_calibration
        self.show_devices = show_devices
        self.show_about = show_about

        # Get the directory of the current script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        icon_dir = os.path.join(current_dir, "assets", "icons")

        # Load icons
        self.scale_icon = PhotoImage(file=os.path.join(icon_dir, "devices-solid-24.png"))
        self.standard_icon = PhotoImage(file=os.path.join(icon_dir, "list-ul-regular-24.png"))
        self.calibration_icon = PhotoImage(file=os.path.join(icon_dir, "target-lock-regular-24.png"))
        self.devices_icon = PhotoImage(file=os.path.join(icon_dir, "devices-solid-24.png"))
        self.about_icon = PhotoImage(file=os.path.join(icon_dir, "info-square-regular-24.png"))

        # Create a frame for the sidebar
        self.sidebar_frame = tk.Frame(self.master, width=200, bg='lightgray')
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar_frame.pack_propagate(False)  # Prevent the frame from resizing to fit its contents
        
        # Sidebar device button
        self.create_button("Scale", self.scale_icon, self.show_scale, True)

        self.menu_label = tk.Label(self.sidebar_frame, padx=10, pady=10, font=('Segoe UI', 10, 'bold'), text='Settings', bg='lightgray', anchor='w').pack(fill=tk.X)

        # Sidebar buttons
        self.create_button("Part Standard", self.standard_icon, self.show_standard)
        self.create_button("Calibration", self.calibration_icon, self.show_calibration)
        self.create_button("Devices", self.devices_icon, self.show_devices)
        self.create_button("About", self.about_icon, self.show_about)

    # Function to create a blue strip effect
    def create_strip(self, button):
        # Remove existing strip if any
        for widget in self.sidebar_frame.winfo_children():
            if isinstance(widget, tk.Frame) and widget.cget("bg") == "blue":
                widget.destroy()
        # Create a new blue strip
        strip = tk.Frame(self.sidebar_frame, width=5, bg='blue')
        strip.place(x=0, y=button.winfo_y() + (button.winfo_height() // 4), height=button.winfo_height() // 2)
        return strip

    def create_button(self, text, image, command, isFirst=False):
        button = tk.Button(
            self.sidebar_frame,
            padx=10,
            pady=10,
            text=text,
            image=image,
            compound=tk.LEFT,
            command=lambda: [command(), self.create_strip(button)],
            relief=tk.FLAT,
            bg='lightgray',
            anchor='w',
        )
        button.pack(fill=tk.X, pady=(24, 0) if isFirst else 0)
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

        if isFirst == True:
            self.sidebar_frame.after(100, lambda: self.create_strip(button))
