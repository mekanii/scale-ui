import tkinter as tk
from tkinter import simpledialog, messagebox
from include.button_hover import on_enter, on_leave
from include.frame_hover import frame_selected, frame_enter, frame_leave
import json  # Add this import for JSON handling

class DevicesContent:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg='white')
        self.frame.pack(pady=10, fill=tk.BOTH, expand=True)

        # Create and configure content label
        self.content_label = tk.Label(self.frame, text="Devices", font=("Segoe UI", 24), anchor='w', bg='white')
        self.content_label.pack(pady=10, anchor='w')

        # Add buttons inline with commands to open dialog and reload data
        button_frame = tk.Frame(self.frame, bg='white')
        button_frame.pack(pady=10, fill=tk.X)

        self.add_button = tk.Button(button_frame, padx=10, pady=2, text="Add", bg='lightgray', relief=tk.FLAT, font=('Segoe UI', 10), command=self.open_dialog)
        self.reload_button = tk.Button(button_frame, padx=10, pady=2, text="Reload", bg='lightgray', relief=tk.FLAT, font=('Segoe UI', 10), command=self.load_data)
        self.add_button.pack(side=tk.LEFT, padx=(0, 5))
        self.reload_button.pack(side=tk.LEFT, padx=5)

        self.add_button.bind("<Enter>", on_enter)
        self.add_button.bind("<Leave>", on_leave)
        self.reload_button.bind("<Enter>", on_enter)
        self.reload_button.bind("<Leave>", on_leave)

        # Create a new frame for the data list
        self.list_frame = tk.Frame(self.frame, bg='white', width=450)
        self.list_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.list_frame.pack_propagate(False)

        self.load_data()

        # # Create a new frame for the data table
        # self.table_frame = tk.Frame(self.frame)
        # self.table_frame.pack(pady=10, fill=tk.X)  # Allow the table frame to expand only in width

        # # Create table headers
        # self.headers = ["Address", "Action"]
        # for col in range(len(self.headers)):
        #     header_label = tk.Label(self.table_frame, text=self.headers[col], borderwidth=0, font=('Segoe UI', 10, 'bold'), bg='#007bff', fg='white', padx=20 if (col == 0 or col == len(self.headers) - 1) else 0, pady=10)
        #     header_label.grid(row=0, column=col, sticky="nsew", padx=(0, 1))
        
        # # Configure grid weights for proper resizing
        # for col in range(len(self.headers) - 1):
        #     self.table_frame.grid_columnconfigure(col, weight=0 if col == len(self.headers) - 1 else 1)  # Prevent the first columns to expand
        
        # # self.table_frame.grid_columnconfigure(len(self.headers) - 1, weight=0)  # Prevent the last column to expand
        
        # # Load initial data from config.json
        # self.load_data()
    
    def load_data(self):
        """Fetch data from config.json and populate the list."""
        try:
            with open('config.json', 'r') as file:  # Open config.json for reading
                response_json = json.load(file)  # Load JSON data
                data = response_json.get('address', [])  # Get the 'address' field
                self.default_address = response_json.get('default', None)  # Store the default address

            # Clear existing list data
            for widget in self.list_frame.winfo_children():
                widget.destroy()

            # Populate the list with data
            for list_index, address in enumerate(data):
                item_frame = tk.Frame(self.list_frame, bg='white')
                item_frame.pack(fill=tk.X)
                data_label = tk.Label(
                    item_frame,
                    padx=10,
                    pady=10,
                    text=address+' (default)' if address == self.default_address else address,
                    font=('Segoe UI', 10),
                    bg='white',
                    anchor='w',
                )
                data_label.pack(fill=tk.X)
                data_label.bind('<Enter>', frame_enter)
                data_label.bind('<Leave>', frame_leave)
                data_label.bind('<Button-1>', frame_selected)

                action_frame = tk.Frame(item_frame, bg='#f1f2f3')

                default_button = tk.Button(
                    action_frame,
                    padx=10,
                    pady=2,
                    text="Default",
                    command=lambda addr=address: self.set_default(addr),
                    bg='lightgray',
                    font=('Segoe UI', 10),
                    relief=tk.FLAT
                )

                modify_button = tk.Button(
                    action_frame,
                    padx=10,
                    pady=2,
                    text="Modify",
                    command=lambda addr=address: self.open_dialog(addr),
                    bg='lightgray',
                    font=('Segoe UI', 10),
                    relief=tk.FLAT
                )

                delete_button = tk.Button(
                    action_frame,
                    padx=10,
                    pady=2,
                    text="Delete",
                    command=lambda addr=address: self.delete_entry(addr),
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

                # Disable the default button if the address is the default
                if address == self.default_address:
                    default_button.config(state=tk.DISABLED)

                default_button.pack(side=tk.RIGHT, padx=(0, 3), pady=(0, 10))
                default_button.bind("<Enter>", on_enter)
                default_button.bind("<Leave>", on_leave)

                action_frame.pack(fill=tk.X)
                action_frame.pack_forget()

        except (FileNotFoundError, json.JSONDecodeError) as e:
            messagebox.showerror("Error", f"Failed to load data: {e}")
            self.show_no_data()
    
    # def load_data(self):
    #     """Fetch data from config.json and populate the table."""
    #     try:
    #         with open('config.json', 'r') as file:  # Open config.json for reading
    #             response_json = json.load(file)  # Load JSON data
    #             data = response_json.get('address', [])  # Get the 'address' field
    #             self.default_address = response_json.get('default', None)  # Store the default address

    #         # Clear existing table data
    #         for widget in self.table_frame.winfo_children():
    #             if widget.grid_info()['row'] > 0:
    #                 widget.destroy()

    #         # Populate the table with data
    #         for row_index, address in enumerate(data):
    #             data_label = tk.Label(self.table_frame, text=address+' (default)' if address == self.default_address else address, borderwidth=0, font=('Segoe UI', 10), bg='#eaebec' if row_index % 2 == 0 else '#f5f6f7', padx=20, pady=10)
    #             data_label.grid(row=row_index + 1, column=0, sticky="nsew", padx=(0, 1))

    #             # Add action buttons for update and delete
    #             action_frame = tk.Frame(self.table_frame, bg='#eaebec' if row_index % 2 == 0 else '#f5f6f7')
    #             default_button = tk.Button(action_frame, padx=10, pady=2, text="Default", bg='lightgray', font=('Segoe UI', 10), relief=tk.FLAT, command=lambda addr=address: self.set_default(addr))
    #             update_button = tk.Button(action_frame, padx=10, pady=2, text="Update", bg='lightgray', font=('Segoe UI', 10), relief=tk.FLAT, command=lambda addr=address: self.open_dialog(addr))
    #             delete_button = tk.Button(action_frame, padx=10, pady=2, text="Delete", bg='lightgray', font=('Segoe UI', 10), relief=tk.FLAT, command=lambda addr=address: self.delete_entry(addr))
                
    #             # Disable the default button if the address is the default
    #             if address == self.default_address:
    #                 default_button.config(state=tk.DISABLED)
                    
    #             default_button.pack(side=tk.LEFT, padx=(6, 3), pady=2)  # Add Default button
    #             update_button.pack(side=tk.LEFT, padx=(3, 3), pady=2)
    #             delete_button.pack(side=tk.LEFT, padx=(3, 6), pady=2)

    #             default_button.bind("<Enter>", on_enter)
    #             default_button.bind("<Leave>", on_leave)
    #             update_button.bind("<Enter>", on_enter)
    #             update_button.bind("<Leave>", on_leave)
    #             delete_button.bind("<Enter>", on_enter)
    #             delete_button.bind("<Leave>", on_leave)
    #             action_frame.grid(row=row_index + 1, column=1, sticky="nsew", padx=(0, 1))

    #     except (FileNotFoundError, json.JSONDecodeError) as e:
    #         messagebox.showerror("Error", f"Failed to load data: {e}")
    #         self.show_no_data()
    
    def show_no_data(self):
        """Show 'No Data' message in the table if no data is available."""
        # if not self.table_frame.winfo_children():
        # no_data_label = tk.Label(self.table_frame, text="No Data", font=('Segoe UI', 10), bg='#eaebec', anchor='w')
        # no_data_label.grid(row=1, column=0, columnspan=len(self.headers), sticky="nsew", padx=20, pady=10)
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

    # Add the new method to set the default address
    def set_default(self, address):
        """Set the selected address as the default in config.json."""
        with open('config.json', 'r+') as file:
            response_json = json.load(file)
            response_json['default'] = address  # Update the default address
            file.seek(0)
            json.dump(response_json, file, indent=4)
            file.truncate()

        messagebox.showinfo("Success", f"Default address set to: {address}")

        # Add (default) suffix and disable the default button for the newly set default address
        for frame in self.list_frame.winfo_children():
            if isinstance(frame, tk.Frame):
                for widget in frame.winfo_children():
                    if isinstance(widget, tk.Label):
                        address_label = widget.cget("text") # Get the address from the first child
                        if address == address_label:
                            widget.config(text=address_label+' (default)') # Add default suffix only the selected Default button
                        else:
                            if address_label.endswith(' (default)'):
                                widget.config(text=address_label.replace(' (default)', ''))
                    if isinstance(widget, tk.Frame):
                        for btn in widget.winfo_children():
                            if btn.cget("text") == "Default" and address == address_label:
                                btn.config(state=tk.DISABLED)  # Disable only the selected Default button
                            else:
                                btn.config(state=tk.NORMAL)

        # for widget in self.table_frame.winfo_children():
        #     if isinstance(widget, tk.Label):
        #         address_label = widget.cget("text") # Get the address from the first child
        #         if address == address_label:
        #             widget.config(text=address_label+' (default)') # Add default suffix only the selected Default button
        #         else:
        #             if address_label.endswith(' (default)'):
        #                 widget.config(text=address_label.replace(' (default)', ''))
        #     if isinstance(widget, tk.Frame):
        #         for btn in widget.winfo_children():
        #             if btn.cget("text") == "Default" and address == address_label:
        #                 btn.config(state=tk.DISABLED)  # Disable only the selected Default button
        #             else:
        #                 btn.config(state=tk.NORMAL)
    
    def open_dialog(self, address=None):
        """Open dialog for creating or updating an entry."""
        # Create a new top-level window for the dialog
        dialog = tk.Toplevel(self.frame, padx=10, bg='white')
        dialog.title("Add Address")

        # Set minimum width and height
        dialog.minsize(width=300, height=150)  # Minimum width of 300 pixels

        # Center the dialog on the parent window
        self.center_dialog(dialog)

        address_label = tk.Label(dialog, text="Address", font=('Segoe UI', 10), bg='white')
        address_label.pack(pady=(10, 0), anchor='w')
        address_frame = tk.Frame(dialog, highlightthickness=1, bg='white')
        address_frame.config(highlightbackground='darkgray', highlightcolor='darkgray')
        address_frame.pack(fill=tk.X)
        address_entry = tk.Entry(address_frame, font=('Segoe UI', 10), relief=tk.FLAT)
        address_entry.pack(padx=5, pady=5, fill=tk.X)

        # Populate field if updating
        if address:
            address_entry.insert(0, address)

        tk.Button(dialog, padx=10, pady=5, bg='lightgray', font=('Segoe UI', 10), text="Submit", command=lambda: self.submit(address_entry.get(), dialog, address), relief=tk.FLAT).pack(side=tk.LEFT)  # Submit button on the left
        tk.Button(dialog, padx=10, pady=5, bg='lightgray', font=('Segoe UI', 10), text="Cancel", command=dialog.destroy, relief=tk.FLAT).pack(side=tk.RIGHT, padx=(5, 0))  # Cancel button on the right

    def submit(self, address, dialog, entry=None):
        """Handle the submission logic here."""
        with open('config.json', 'r+') as file:  # Open config.json for reading and writing
            response_json = json.load(file)
            if entry:  # Update existing entry
                # Check if the address being updated is the default
                if entry == response_json['default']:
                    response_json['default'] = address  # Update the default address if the current entry is the default

                # Update the address in the list
                response_json['address'] = [address if addr == entry else addr for addr in response_json['address']]  # Update address
            else:  # Create new entry
                response_json['address'].append(address)  # Add new address

            file.seek(0)  # Move to the beginning of the file
            json.dump(response_json, file, indent=4)  # Write updated data
            file.truncate()  # Remove any leftover data

        messagebox.showinfo("Success", "Entry saved successfully!")
        self.load_data()  # Reload data to reflect changes
        dialog.destroy()  # Close the dialog after submission

    def delete_entry(self, address):
        """Delete an entry by address."""
        with open('config.json', 'r+') as file:
            response_json = json.load(file)
            response_json['address'] = [addr for addr in response_json['address'] if addr != address]  # Remove address
            file.seek(0)
            json.dump(response_json, file, indent=4)
            file.truncate()

        messagebox.showinfo("Success", "Entry deleted successfully!")
        self.load_data()  # Reload data to reflect changes

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