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

        self.start_icon = PhotoImage(file=os.path.join(icon_dir, "play-solid-36.png"))
        self.start_button = tk.Button(
            l_frame,
            padx=10,
            pady=10,
            anchor='w',
            justify='left',
            image=self.start_icon,
            compound=tk.LEFT,
            text="Start Calibration",
            bg='white',
            relief=tk.FLAT,
            font=('Segoe UI', 10),
            command=self.init_calibration
        )
        self.start_button.pack(pady=5, fill=tk.X)
        self.start_button.bind("<Enter>", lambda e: on_enter(e, color='#f1f2f3'))
        self.start_button.bind("<Leave>", lambda e: on_leave(e, color='white'))

        # Create a new frame for the data list
        self.log_frame = tk.Frame(l_frame, bg='white')
        self.log_frame.pack(fill=tk.X)

    def init_calibration(self):
        try:
            with open('config.json', 'r') as file:
                json_data = json.load(file)
                base_api_url = json_data.get('default', None)

                # Clear existing table data
                for widget in self.log_frame.winfo_children():
                    widget.destroy()

                # Display initialization instructions on log_frame
                self.log_label = tk.Label(self.log_frame, anchor='w', justify='left', text="Initialize calibration.", font=('Segoe UI', 10), bg='white')
                self.log_label.pack(fill=tk.X)

                self.log_label = tk.Label(self.log_frame, anchor='w', justify='left', text="Place the load cell on a level stable surface.", font=('Segoe UI', 10), bg='white')
                self.log_label.pack(fill=tk.X)

                self.log_label = tk.Label(self.log_frame, anchor='w', justify='left', text="Remove any load applied to the load cell.", font=('Segoe UI', 10, "bold"), bg='white')
                self.log_label.pack(fill=tk.X)

                self.dot_text = tk.Label(self.log_frame, anchor='w', justify='left', text="", font=('Segoe UI', 10), bg='white')
                self.dot_text.pack(fill=tk.X)
                
                # Start appending dots synchronously
                for _ in range(10):
                    current_text =  self.dot_text.cget('text')
                    self.dot_text.config(text=current_text + '.')
                    self.frame.update()  # Update the frame to reflect changes
                    self.frame.after(500)  # Wait for 500 milliseconds

                response = requests.get(f"http://{base_api_url}/initCalibration")
                response.raise_for_status()  # Raise an error for bad responses
            
                # Parse the response JSON
                response_json = response.json()  # Assuming the response is in JSON format
                # data = response_json.get('data', "")  # Get the 'data' field, default to an empty list if not found

                # Update the log frame
                self.log_label = tk.Label(self.log_frame, anchor='w', justify='left', text="Initialize complete.", font=('Segoe UI', 10), bg='white')
                self.log_label.pack(fill=tk.X)

                self.log_label = tk.Label(self.log_frame, anchor='w', justify='left', text="Place **Known Weight** on the loadcell.", font=('Segoe UI', 10, "bold"), bg='white')
                self.log_label.pack(fill=tk.X)

                self.dot_text = tk.Label(self.log_frame, anchor='w', justify='left', text="", font=('Segoe UI', 10), bg='white')
                self.dot_text.pack(fill=tk.X)
                
                # Start appending dots synchronously
                for _ in range(10):
                    current_text =  self.dot_text.cget('text')
                    self.dot_text.config(text=current_text + '.')
                    self.frame.update()  # Update the frame to reflect changes
                    self.frame.after(500)  # Wait for 500 milliseconds

                self.open_dialog()

        except requests.RequestException as e:
            messagebox.showerror("Error", f"Failed to load data: {e}")

    def open_dialog(self):
        """Open dialog for creating or updating an entry."""
        # Create a new top-level window for the dialog
        dialog = tk.Toplevel(self.frame, padx=10, bg='white')
        dialog.title("Add New Device")

        # Set minimum width and height
        dialog.minsize(width=300, height=150)  # Minimum width of 300 pixels

        # Center the dialog on the parent window
        self.center_dialog(dialog)

        known_weight_label = tk.Label(dialog, text="IP Address", font=('Segoe UI', 10), bg='white')
        known_weight_label.pack(pady=(10, 0), anchor='w')
        known_weight_frame = tk.Frame(dialog, highlightthickness=1, bg='white')
        known_weight_frame.config(highlightbackground='darkgray', highlightcolor='darkgray')
        known_weight_frame.pack(fill=tk.X)
        known_weight_entry = tk.Entry(known_weight_frame, font=('Segoe UI', 10), relief=tk.FLAT)
        known_weight_entry.pack(padx=5, pady=5, fill=tk.X)

        button_frame = tk.Frame(dialog, bg='white')
        button_frame.pack(pady=10, fill=tk.X, side=tk.BOTTOM)
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

        submit_button = tk.Button(button_frame, padx=10, pady=5, bg='lightgray', font=('Segoe UI', 10), text="Submit", command=lambda: self.submit(known_weight_entry.get(), dialog), relief=tk.FLAT)
        submit_button.grid(padx=(0, 5), row=0, column=0, sticky='ew')
        submit_button.bind("<Enter>", on_enter)
        submit_button.bind("<Leave>", on_leave)
        
        cancel_button = tk.Button(button_frame, padx=10, pady=5, bg='lightgray', font=('Segoe UI', 10), text="Cancel", command=lambda: [dialog.destroy(), *map(lambda child: child.destroy(), self.log_frame.winfo_children())], relief=tk.FLAT)
        cancel_button.grid(padx=(5, 0), row=0, column=1, sticky='ew')
        cancel_button.bind("<Enter>", on_enter)
        cancel_button.bind("<Leave>", on_leave)

    def submit(self, known_weight, dialog):
        """Handle the submission logic here."""
        try:
            with open('config.json', 'r') as file:
                dialog.destroy()
                json_data = json.load(file)
                base_api_url = json_data.get('default', None)

                # Update existing entry
                response = requests.post(f"http://{base_api_url}/calibrationFactor?knownWeight={known_weight}")
                
                print(response.json())
                response_json = response.json()
                data = response_json.get('data', 0.0)
                if response.status_code in (200, 201):
                    
                    self.log_label = tk.Label(self.log_frame, anchor='w', justify='left', text="New calibration factor has been set to: " + str(data), font=('Segoe UI', 10), bg='white')
                    self.log_label.pack(fill=tk.X)

                    self.log_label = tk.Label(self.log_frame, anchor='w', justify='left', text="Calibation complete.", font=('Segoe UI', 10), bg='white')
                    self.log_label.pack(fill=tk.X)
                    
                    self.log_label.after(2000, lambda: messagebox.showinfo("Success", "Entry saved successfully!"))
                else:
                    messagebox.showerror("Error", "Failed to save entry.")

        except requests.RequestException as e:
            messagebox.showerror("Error", f"Failed to save entry: {e}")

    def center_dialog(self, dialog):
        # Center the dialog on the parent window
        parent_width = self.frame.winfo_width()
        parent_height = self.frame.winfo_height()
        parent_x = self.frame.winfo_x()
        parent_y = self.frame.winfo_y()

        dialog_width = 300  # Set a fixed width for the dialog
        dialog_height = 200  # Set a fixed height for the dialog

        # Calculate the position
        x = parent_x + (parent_width // 2) - (dialog_width // 2)
        y = parent_y + (parent_height // 2) - (dialog_height // 2)

        dialog.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")  # Set the size and position