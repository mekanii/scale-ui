import tkinter as tk

def on_enter(event, color='darkgray'):
    """Change button color on hover."""
    if event.widget['state'] != 'disabled':
        event.widget.config(bg=color)  # Change to dark gray on hover

def on_leave(event, color='lightgray'):
    """Reset button color when not hovered."""
    event.widget.config(bg=color)  # Reset to light gray when not hovered