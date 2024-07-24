import tkinter as tk

def frame_enter(event, color='#eaebec'):
    """Change bg color on hover."""
    if event.widget.cget('bg') != '#f1f2f3':  # Only change color if not selected
        event.widget.config(bg=color)  # Change to light gray on hover

def frame_leave(event, color='white'):
    """Reset bg color when not hovered."""
    if event.widget.cget('bg') != '#f1f2f3':  # Only change color if not selected
        event.widget.config(bg=color)  # Reset to white when not hovered

def frame_selected(event, color='#f1f2f3'):
    """Change bg color when selected."""

    for frame in event.widget.master.master.winfo_children():
        if isinstance(frame, tk.Frame):
            for widget in frame.winfo_children():
                if isinstance(widget, tk.Label) and widget.cget('bg') == '#f1f2f3':
                    widget.config(bg='white')  # Reset to white when not selected
                if isinstance(widget, tk.Frame):
                    widget.pack_forget()
    
    event.widget.config(bg=color)  # Change to dark gray when selected
    
    for widget in event.widget.master.winfo_children():
        if isinstance(widget, tk.Frame):
            widget.pack(fill=tk.X)