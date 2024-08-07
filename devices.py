import tkinter as tk
from tkinter import simpledialog, messagebox, PhotoImage
from include.button_hover import on_enter, on_leave
from include.frame_hover import frame_selected, frame_enter, frame_leave
import os
import json

class DevicesContent:
    def __init__(self, parent):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        icon_dir = os.path.join(current_dir, "assets", "icons")

        self.frame = tk.Frame(parent, bg='white')
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)
        # self.frame.pack(pady=10)

        l_frame = tk.Frame(self.frame, bg='white')
        l_frame.grid(row=0, padx=(0, 10), pady=10, column=0, sticky='nsew')
        r_frame = tk.Frame(self.frame, bg='white')
        r_frame.grid(row=0, pady=10, column=1, sticky='nsew')

        # Create and configure content label
        self.content_label = tk.Label(l_frame, text="Devices", font=("Segoe UI", 24), anchor='w', bg='white', fg='black')
        self.content_label.pack(pady=10, anchor='w')

        self.add_icon = PhotoImage(file=os.path.join(icon_dir, "add-solid-36.png"))
        self.add_button = tk.Button(
            l_frame,
            padx=10,
            anchor='w',
            justify='left',
            image=self.add_icon,
            compound=tk.LEFT,
            text="Add Device\nSee IP Address on device Settings",
            bg='white',
            relief=tk.FLAT,
            font=('Segoe UI', 10),
            command=self.open_dialog,
            fg='black'
        )
        self.add_button.pack(pady=5, ipady=10, fill=tk.X)

        self.reload_icon = PhotoImage(file=os.path.join(icon_dir, "refresh-solid-36.png"))
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
            command=self.load_data,
            fg='black'
        )
        self.reload_button.pack(pady=5, ipady=10, fill=tk.X)

        self.add_button.bind("<Enter>", lambda e: on_enter(e, color='#f1f2f3'))
        self.add_button.bind("<Leave>", lambda e: on_leave(e, color='white'))
        self.reload_button.bind("<Enter>", lambda e: on_enter(e, color='#f1f2f3'))
        self.reload_button.bind("<Leave>", lambda e: on_leave(e, color='white'))

        # Create a new frame for the data list
        self.list_frame = tk.Frame(l_frame, bg='white')
        self.list_frame.pack(fill=tk.X)

        self.load_data()

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

            item_count_label = tk.Label(
                self.list_frame,
                text=str(len(data))+' devices found',
                font=('Segoe UI', 14),
                bg='white',
                anchor='w',
                fg='black'
            )
            item_count_label.pack(pady=(20, 5), fill=tk.X)

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
                    fg='black'
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
                    relief=tk.FLAT,
                    bd=0,
                    borderwidth=0,
                    highlightthickness=0,
                    fg='black'
                )

                modify_button = tk.Button(
                    action_frame,
                    padx=10,
                    pady=2,
                    text="Modify",
                    command=lambda addr=address: self.open_dialog(addr),
                    bg='lightgray',
                    font=('Segoe UI', 10),
                    relief=tk.FLAT,
                    bd=0,
                    borderwidth=0,
                    highlightthickness=0,
                    fg='black'
                )

                delete_button = tk.Button(
                    action_frame,
                    padx=10,
                    pady=2,
                    text="Delete",
                    command=lambda addr=address: self.delete_entry(addr),
                    bg='lightgray',
                    font=('Segoe UI', 10),
                    relief=tk.FLAT,
                    bd=0,
                    borderwidth=0,
                    highlightthickness=0,
                    fg='black'
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
            fg='black'
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

    def open_dialog(self, address=None):
        """Open dialog for creating or updating an entry."""
        # Create a new top-level window for the dialog
        dialog = tk.Toplevel(self.frame, padx=10, bg='white')
        dialog.title("Add New Device")

        # Set minimum width and height
        dialog.minsize(width=300, height=150)  # Minimum width of 300 pixels

        # Center the dialog on the parent window
        self.center_dialog(dialog)

        address_label = tk.Label(
            dialog,
            text="IP Address",
            font=('Segoe UI', 10),
            bg='white',
            fg='black'
        )
        address_label.pack(pady=(10, 0), anchor='w')
        
        address_frame = tk.Frame(dialog, highlightthickness=1, bg='white')
        address_frame.config(highlightbackground='darkgray', highlightcolor='darkgray')
        address_frame.pack(fill=tk.X)

        address_entry = tk.Entry(
            address_frame,
            font=('Segoe UI', 10),
            relief=tk.FLAT,
            highlightthickness=0
        )
        address_entry.pack(padx=5, pady=5, fill=tk.X)

        # Populate field if updating
        if address:
            address_entry.insert(0, address)

        button_frame = tk.Frame(dialog, bg='white')
        button_frame.pack(pady=10, fill=tk.X, side=tk.BOTTOM)
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

        submit_button = tk.Button(
            button_frame,
            padx=10,
            pady=5,
            bg='lightgray',
            font=('Segoe UI', 10),
            text="Submit",
            command=lambda: self.submit(address_entry.get(), dialog, address),
            relief=tk.FLAT,
            fg='black'
        )
        submit_button.grid(padx=(0, 5), row=0, column=0, sticky='ew')
        submit_button.bind("<Enter>", on_enter)
        submit_button.bind("<Leave>", on_leave)
        
        cancel_button = tk.Button(
            button_frame,
            padx=10,
            pady=5,
            bg='lightgray',
            font=('Segoe UI', 10),
            text="Cancel",
            command=dialog.destroy,
            relief=tk.FLAT,
            fg='black'
        )
        cancel_button.grid(padx=(5, 0), row=0, column=1, sticky='ew')
        cancel_button.bind("<Enter>", on_enter)
        cancel_button.bind("<Leave>", on_leave)

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