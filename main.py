import os
import tkinter as tk
from tkinter import font
from sidebar import Sidebar
from scale import ScaleContent
from standard import StandardContent
from calibration import CalibrationContent
from devices import DevicesContent
from about import AboutContent

class SettingsWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Settings")
        self.master.geometry("800x600")  # Set an initial size
        self.master.state('normal')  # Ensure the window is in normal state
        self.master.resizable(True, True)  # Allow resizing
        self.master.configure(bg='white')  # Set the background color of the main window

        # Force light theme
        self.master.tk_setPalette(background='white', foreground='black', activeBackground='lightgray', activeForeground='black')

        # Create sidebar
        self.sidebar = Sidebar(self.master, self.show_scale_content, self.show_standard_content, self.show_calibration_content, self.show_devices_content, self.show_about_content)

        # Create a frame for the main content
        self.content_frame = tk.Frame(self.master, bg='white')
        self.content_frame.pack(padx=10, expand=True, fill=tk.BOTH)

        # Initialize content
        self.current_content = None
        self.show_scale_content()  # Show default content

    def show_scale_content(self):
        self.clear_content()  # Clear previous content
        self.current_content = ScaleContent(self.content_frame)

    def show_standard_content(self):
        self.clear_content()  # Clear previous content
        self.current_content = StandardContent(self.content_frame)

    def show_calibration_content(self):
        self.clear_content()  # Clear previous content
        self.current_content = CalibrationContent(self.content_frame)

    def show_devices_content(self):
        self.clear_content()  # Clear previous content
        self.current_content = DevicesContent(self.content_frame)

    def show_about_content(self):
        self.clear_content()  # Clear previous content
        self.current_content = AboutContent(self.content_frame)

    def clear_content(self):
        # Clear the content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SettingsWindow(root)
    root.mainloop()