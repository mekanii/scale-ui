import tkinter as tk

def on_enter(event):
    """Change button color on hover."""
    if event.widget['state'] != 'disabled':
        event.widget.config(bg='darkgray')  # Change to dark gray on hover

def on_leave(event):
    """Reset button color when not hovered."""
    event.widget.config(bg='lightgray')  # Reset to light gray when not hovered