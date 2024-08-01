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

        # Create and configure content label
        self.content_label = tk.Label(l_frame, text="Part Standards", font=("Segoe UI", 24), anchor='w', bg='white')
        self.content_label.pack(pady=10, anchor='w')

        self.add_icon = PhotoImage(file=os.path.join(icon_dir, "add-solid-36.png"))
        self.add_button = tk.Button(
            l_frame,
            padx=10,
            pady=10,
            anchor='w',
            justify='left',
            image=self.add_icon,
            compound=tk.LEFT,
            text="Add Standard",
            bg='white',
            relief=tk.FLAT,
            font=('Segoe UI', 10),
            command=self.open_dialog
        )
        self.add_button.pack(pady=5, fill=tk.X)

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
            command=self.load_data
        )
        self.reload_button.pack(pady=5, fill=tk.X)

        self.add_button.bind("<Enter>", lambda e: on_enter(e, color='#f1f2f3'))
        self.add_button.bind("<Leave>", lambda e: on_leave(e, color='white'))
        self.reload_button.bind("<Enter>", lambda e: on_enter(e, color='#f1f2f3'))
        self.reload_button.bind("<Leave>", lambda e: on_leave(e, color='white'))

        # Create a new frame for the data list
        self.list_frame = tk.Frame(l_frame, bg='white')
        self.list_frame.pack(fill=tk.X)

        self.load_data()
    
    def load_data(self):
        """Fetch data from API and populate the table."""
        try:
            with open('config.json', 'r') as file:
                json_data = json.load(file)
                base_api_url = json_data.get('default', None)

                response = requests.get(f"http://{base_api_url}/parts")
                
                # Raise an error for bad responses
                response.raise_for_status()
            
                # Parse the response JSON
                response_json = response.json()

                # Get the 'data' field, default to an empty list if not found
                data = response_json.get('data', [])

                # Clear existing table data
                for widget in self.list_frame.winfo_children():
                    widget.destroy()

                item_count_label = tk.Label(
                    self.list_frame,
                    text=str(len(data))+' part standards found',
                    font=('Segoe UI', 14),
                    bg='white',
                    anchor='w'
                )
                item_count_label.pack(pady=(20, 5), fill=tk.X)

                # Populate the list with data
                for row_index, row in enumerate(data):
                    item_frame = tk.Frame(self.list_frame, bg='white')
                    item_frame.pack(fill=tk.X)
                    
                    # values = [row['id'], row['name'], row['std'], row['unit']]
                    
                    data_label = tk.Label(
                        item_frame,
                        padx=10,
                        pady=10,
                        anchor='w',
                        justify='left',
                        text=f"{row['name']}\n{row['std']} {row['unit']}",
                        bg='white',
                        font=('Segoe UI', 10)
                    )
                    data_label.pack(fill=tk.X)
                    data_label.bind('<Enter>', frame_enter)
                    data_label.bind('<Leave>', frame_leave)
                    data_label.bind('<Button-1>', frame_selected)
                    
                    action_frame = tk.Frame(item_frame, bg='#f1f2f3')

                    modify_button = tk.Button(
                        action_frame,
                        padx=10,
                        pady=2,
                        text="Modify",
                        command=lambda r=row: self.open_dialog(r),
                        bg='lightgray',
                        font=('Segoe UI', 10),
                        relief=tk.FLAT
                    )

                    delete_button = tk.Button(
                        action_frame,
                        padx=10,
                        pady=2,
                        text="Delete",
                        command=lambda r=row: self.delete_entry(r['id']),
                        bg='lightgray',
                        font=('Segoe UI', 10),
                        relief=tk.FLAT
                    )

                    delete_button.pack(side=tk.RIGHT, padx=(3, 6), pady=(0, 10))
                    delete_button.bind("<Enter>", on_enter)
                    delete_button.bind("<Leave>", on_leave)

                    modify_button.pack(side=tk.RIGHT, padx=(3, 3), pady=(0, 10))
                    modify_button.bind("<Enter>", on_enter)
                    modify_button.bind("<Leave>", on_leave)

                    action_frame.pack(fill=tk.X)
                    action_frame.pack_forget()

        except requests.RequestException as e:
            messagebox.showerror("Error", f"Failed to load data: {e}")
            self.show_no_data()
    
    def show_no_data(self):
        """Show 'No Data' message in the table if no data is available."""
           
        data_label = tk.Label(
            self.list_frame,
            padx=10,
            pady=10,
            text="No Data",
            font=('Segoe UI', 10),
            bg='white',
            anchor='w',
        )
        data_label.pack(fill=tk.X)
    
    def open_dialog(self, entry=None):
        """Open dialog for creating or updating an entry."""

        # Create a new top-level window for the dialog
        dialog = tk.Toplevel(self.frame, padx=10, bg='white')
        dialog.title("Add Part Standard")

        # Set minimum width and height
        dialog.minsize(width=300, height=300)  # Minimum width of 300 pixels

        # Center the dialog on the parent window
        self.center_dialog(dialog)
        
        # Create a validation command
        vcmd = (self.frame.register(self.validate_numeric_input), '%P')

        part_name_label = tk.Label(dialog, text="Part Name", font=('Segoe UI', 10), bg='white')
        part_name_label.pack(pady=(10,0), anchor='w')
        part_name_frame = tk.Frame(dialog, highlightthickness=1, bg='white')
        part_name_frame.config(highlightbackground='darkgray', highlightcolor='darkgray')
        part_name_frame.pack(fill=tk.X)
        part_name_entry = tk.Entry(part_name_frame, font=('Segoe UI', 10), relief=tk.FLAT)
        part_name_entry.pack(padx=5, pady=5, fill=tk.X)

        part_std_label = tk.Label(dialog, text="Standard Weight", font=('Segoe UI', 10), bg='white')
        part_std_label.pack(pady=(10,0), anchor='w')
        part_std_frame = tk.Frame(dialog, highlightthickness=1, bg='white')
        part_std_frame.config(highlightbackground='darkgray', highlightcolor='darkgray')
        part_std_frame.pack(fill=tk.X)
        self.part_std_entry = tk.Entry(part_std_frame, validate='key', validatecommand=vcmd, justify='right', font=('Segoe UI', 10), relief=tk.FLAT)
        self.part_std_entry.pack(padx=5, fill=tk.Y, side=tk.LEFT)
        
        tk.Button(
            part_std_frame,
            padx=10,
            pady=5,
            bg='lightgray',
            font=('Segoe UI', 10),
            text="Get weight",
            command=lambda: self.measure(),
            relief=tk.FLAT).pack(side=tk.RIGHT)
        
        part_std_label = tk.Label(dialog, text="Place **Part** on the loadcell.", font=('Segoe UI', 10), bg='white')
        part_std_label.pack(anchor='w')

        unit_label = tk.Label(dialog, text="Unit", font=('Segoe UI', 10), bg='white')
        unit_label.pack(pady=(10,0), anchor='w')
        unit_var = tk.StringVar(value="gr")  # Default value
        unit_gr = tk.Radiobutton(dialog, text="gr", variable=unit_var, value="gr", font=('Segoe UI', 10), bg='white')
        unit_kg = tk.Radiobutton(dialog, text="kg", variable=unit_var, value="kg", font=('Segoe UI', 10), bg='white')
        unit_gr.pack(anchor='w')
        unit_kg.pack(anchor='w')

        # Populate fields if updating
        if entry:
            part_name_entry.insert(0, entry['name'])
            self.part_std_entry.insert(0, entry['std'])
            unit_var.set(entry['unit'])

        tk.Button(
            dialog,
            padx=10,
            pady=5,
            bg='lightgray',
            font=('Segoe UI', 10),
            text="Submit",
            command=lambda: self.submit(part_name_entry.get(), self.part_std_entry.get(), unit_var.get(), dialog, entry),
            relief=tk.FLAT).pack(side=tk.LEFT)  # Submit button on the left
        tk.Button(dialog, padx=10, pady=5, bg='lightgray', font=('Segoe UI', 10), text="Clear", command=lambda: self.clear(part_name_entry, self.part_std_entry, unit_var), relief=tk.FLAT).pack(side=tk.RIGHT, padx=(5, 0))  # Clear button on the right
        tk.Button(dialog, padx=10, pady=5, bg='lightgray', font=('Segoe UI', 10), text="Cancel", command=dialog.destroy, relief=tk.FLAT).pack(side=tk.RIGHT, padx=(5, 0))  # Cancel button on the right

    def validate_numeric_input(self, P):
        """Validate input to allow only numeric values."""
        if P == "" or P.replace('.', '', 1).isdigit():  # Allow empty input or numeric input
            return True
        return False

    def measure(self):
        try:
            with open('config.json', 'r') as file:
                json_data = json.load(file)
                base_api_url = json_data.get('default', None)
                
                response = requests.get(f"http://{base_api_url}/getStableWeight")
                        
                # Raise an error for bad responses
                response.raise_for_status()
            
                # Parse the response JSON
                response_json = response.json()

                # Get the 'data' field, default to an empty list if not found
                data = response_json.get('data', 0)

                print(response_json)

                # Clear the entry and insert the new data
                self.part_std_entry.delete(0, tk.END)
                self.part_std_entry.insert(0, data)
        
        except requests.RequestException as e:
            messagebox.showerror("Error", f"Failed to get data: {e}")
            self.show_no_data()
        
    def submit(self, name, std, unit, dialog, entry=None):
        """Handle the submission logic here."""
        try:
            with open('config.json', 'r') as file:
                json_data = json.load(file)
                base_api_url = json_data.get('default', None)

                # Update existing entry
                if entry:
                    response = requests.put(f"http://{base_api_url}/parts/?id={entry['id']}&name={name}&std={std}&unit={unit}")
                # Create new entry
                else:
                    response = requests.post(f"http://{base_api_url}/parts?name={name}&std={std}&unit={unit}")
                
                print(response.json())
                if response.status_code in (200, 201):
                    messagebox.showinfo("Success", "Entry saved successfully!")
                    self.load_data()  # Reload data to reflect changes
                    dialog.destroy()  # Close the dialog after submission
                else:
                    messagebox.showerror("Error", "Failed to save entry.")

        except requests.RequestException as e:
            messagebox.showerror("Error", f"Failed to save entry: {e}")


    def delete_entry(self, entry_id):
        """Delete an entry by ID."""
        try:
            with open('config.json', 'r') as file:
                json_data = json.load(file)
                base_api_url = json_data.get('default', None)
                
                response = requests.delete(f"http://{base_api_url}/parts/?id={entry_id}")

                if response.status_code in (200, 201):
                    messagebox.showinfo("Success", "Entry deleted successfully!")
                    self.load_data()  # Reload data to reflect changes
                else:
                    messagebox.showerror("Error", "Failed to delete entry.")

        except requests.RequestException as e:
            messagebox.showerror("Error", f"Failed to delete entry: {e}")

    def clear(self, part_name_entry, part_std_entry, unit_var):
        # Clear the input fields
        part_name_entry.delete(0, tk.END)
        part_std_entry.delete(0, tk.END)

        # Optionally reset the unit selection
        unit_var.set("gr")  # Reset the unit selection to the default value "gr"
        # (You can add logic here if needed)

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