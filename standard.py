import tkinter as tk
from tkinter import simpledialog, messagebox
from include.button_hover import on_enter, on_leave
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class StandardContent:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg='white')
        self.frame.pack(pady=10, fill=tk.X)

        # Create and configure content label
        self.content_label = tk.Label(self.frame, text="Part Standard", font=("Segoe UI", 24), anchor='w', bg='white')
        self.content_label.pack(pady=10, anchor='w')

        # Add buttons inline with commands to open dialog and reload data
        button_frame = tk.Frame(self.frame, bg='white')
        button_frame.pack(pady=10, fill=tk.X)

        self.add_button = tk.Button(button_frame, padx=10, pady=5, text="Add", bg='lightgray', relief=tk.FLAT, font=('Segoe UI', 10), command=self.open_dialog)
        self.reload_button = tk.Button(button_frame, padx=10, pady=5, text="Reload", bg='lightgray', relief=tk.FLAT, font=('Segoe UI', 10), command=self.load_data)
        self.add_button.pack(side=tk.LEFT, padx=(0, 5))
        self.reload_button.pack(side=tk.LEFT, padx=5)
        self.add_button.bind("<Enter>", on_enter)
        self.add_button.bind("<Leave>", on_leave)
        self.reload_button.bind("<Enter>", on_enter)
        self.reload_button.bind("<Leave>", on_leave)

        # Create a new frame for the data table
        self.table_frame = tk.Frame(self.frame)
        self.table_frame.pack(pady=10, fill=tk.X)  # Allow the table frame to expand only in width

        # Create table headers
        self.headers = ["ID", "Part Number", "Standard", "Unit", "Action"]
        for col in range(len(self.headers)):
            header_label = tk.Label(self.table_frame, text=self.headers[col], borderwidth=0, font=('Segoe UI', 10, 'bold'), bg='#007bff', fg='white', padx=20 if (col == 0 or col == len(self.headers) - 1) else 0, pady=10)
            header_label.grid(row=0, column=col, sticky="nsew", padx=(0, 1))
        
        # Configure grid weights for proper resizing
        for col in range(len(self.headers) - 1):
            self.table_frame.grid_columnconfigure(col, weight=0 if col == 0 else 1)  # Prevent the first columns to expand
        
        self.table_frame.grid_columnconfigure(len(self.headers) - 1, weight=0)  # Prevent the last column to expand
        
        # Load initial data from API
        self.load_data()
    
    def load_data(self):
        """Fetch data from API and populate the table."""
        api_url = f"{os.getenv('API_BASE_URL')}/parts"  # Replace with your actual API endpoint
        try:
            response = requests.get(api_url)
            response.raise_for_status()  # Raise an error for bad responses
            
            # Parse the response JSON
            response_json = response.json()  # Assuming the response is in JSON format
            data = response_json.get('data', [])  # Get the 'data' field, default to an empty list if not found

            # Clear existing table data
            for widget in self.table_frame.winfo_children():
                if widget.grid_info()['row'] > 0:
                    widget.destroy()

            # Populate the table with data
            for row_index, row in enumerate(data):
                values = [row['id'], row['name'], row['std'], row['unit']]
                for col_index, value in enumerate(values):
                    data_label = tk.Label(self.table_frame, text=(row_index + 1) if col_index == 0 else value, borderwidth=0, font=('Segoe UI', 10), bg='#eaebec' if row_index % 2 == 0 else '#f5f6f7', padx=20 if col_index == 0 else 0, pady=10)
                    data_label.grid(row=row_index + 1, column=col_index, sticky="nsew", padx=(0, 1))

                # Add action buttons for update and delete
                action_frame = tk.Frame(self.table_frame, bg='#eaebec' if row_index % 2 == 0 else '#f5f6f7')
                update_button = tk.Button(action_frame, padx=10, pady=2, text="Update", bg='lightgray', font=('Segoe UI', 10), relief=tk.FLAT, command=lambda r=row: self.open_dialog(r))
                delete_button = tk.Button(action_frame, padx=10, pady=2, text="Delete", bg='lightgray', font=('Segoe UI', 10), relief=tk.FLAT, command=lambda r=row: self.delete_entry(r['id']))
                update_button.pack(side=tk.LEFT, padx=(6, 3), pady=2)
                delete_button.pack(side=tk.LEFT, padx=(3, 6), pady=2)
                update_button.bind("<Enter>", on_enter)
                update_button.bind("<Leave>", on_leave)
                delete_button.bind("<Enter>", on_enter)
                delete_button.bind("<Leave>", on_leave)
                action_frame.grid(row=row_index + 1, column=len(self.headers) - 1, sticky="nsew", padx=(0, 1))
            
            # Configure grid weights for proper resizing
            for col in range(len(self.headers) - 1):
                self.table_frame.grid_columnconfigure(col, weight=0 if col == 0 else 1)  # Prevent the first columns to expand
            
            self.table_frame.grid_columnconfigure(len(self.headers) - 1, weight=0)  # Prevent the last column to expand

        except requests.RequestException as e:
            messagebox.showerror("Error", f"Failed to load data: {e}")
            self.show_no_data()
    
    def show_no_data(self):
        """Show 'No Data' message in the table if no data is available."""
        # if not self.table_frame.winfo_children():
        no_data_label = tk.Label(self.table_frame, text="No Data", font=('Segoe UI', 10), bg='#eaebec', anchor='w')
        no_data_label.grid(row=1, column=0, columnspan=len(self.headers), sticky="nsew", padx=20, pady=10)        
    
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
        part_std_entry = tk.Entry(part_std_frame, validate='key', validatecommand=vcmd, justify='right', font=('Segoe UI', 10), relief=tk.FLAT)
        part_std_entry.pack(padx=5, pady=5, fill=tk.X)

        unit_label = tk.Label(dialog, text="Unit", font=('Segoe UI', 10), bg='white')
        unit_label.pack(pady=(10,0), anchor='w')
        unit_var = tk.StringVar(value="gr")  # Default value
        unit_gr = tk.Radiobutton(dialog, text="gr", variable=unit_var, value="gr", font=('Segoe UI', 10), bg='white')
        unit_kg = tk.Radiobutton(dialog, text="kg", variable=unit_var, value="kg", font=('Segoe UI', 10), bg='white')
        unit_gr.pack(anchor='w')
        unit_kg.pack(anchor='w')

        # Populate fields if updating
        if entry:
            part_name_entry.insert(0, entry['part_name'])
            part_std_entry.insert(0, entry['part_std'])
            unit_var.set(entry['unit'])

        tk.Button(dialog, padx=10, pady=5, bg='lightgray', font=('Segoe UI', 10), text="Submit", command=lambda: self.submit(part_name_entry.get(), part_std_entry.get(), unit_var.get(), dialog), relief=tk.FLAT).pack(side=tk.LEFT)  # Submit button on the left
        tk.Button(dialog, padx=10, pady=5, bg='lightgray', font=('Segoe UI', 10), text="Clear", command=lambda: self.clear(part_name_entry, part_std_entry, unit_var), relief=tk.FLAT).pack(side=tk.RIGHT, padx=(5, 0))  # Clear button on the right
        tk.Button(dialog, padx=10, pady=5, bg='lightgray', font=('Segoe UI', 10), text="Cancel", command=dialog.destroy, relief=tk.FLAT).pack(side=tk.RIGHT, padx=(5, 0))  # Cancel button on the right

    def validate_numeric_input(self, P):
        """Validate input to allow only numeric values."""
        if P == "" or P.replace('.', '', 1).isdigit():  # Allow empty input or numeric input
            return True
        return False
        
    def submit(self, part_name, part_std, unit, dialog, entry=None):
        """Handle the submission logic here."""
        if entry:  # Update existing entry
            # Call API to update the entry with parameters in the URL
            api_url = api_url = f"{os.getenv('API_BASE_URL')}/parts/?id={entry['id']}?name={part_name}&std={part_std}&unit={unit}"
            response = requests.put(api_url)
        else:  # Create new entry
            # Call API to create a new entry with parameters in the URL
            api_url = f"{os.getenv('API_BASE_URL')}/parts?name={part_name}&std={part_std}&unit={unit}"
            response = requests.post(api_url)

        print(response.json())

        if response.status_code in (200, 201):  # Check for success
            messagebox.showinfo("Success", "Entry saved successfully!")
            self.load_data()  # Reload data to reflect changes
            dialog.destroy()  # Close the dialog after submission
        else:
            messagebox.showerror("Error", "Failed to save entry.")

    def delete_entry(self, entry_id):
        """Delete an entry by ID."""
        api_url = f"{os.getenv('API_BASE_URL')}/parts/?id={entry_id}"
        response = requests.delete(api_url)

        print(api_url)
        print(response.json())

        if response.status_code == 200:  # No content on successful delete
            messagebox.showinfo("Success", "Entry deleted successfully!")
            self.load_data()  # Reload data to reflect changes
        else:
            messagebox.showerror("Error", "Failed to delete entry.")

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