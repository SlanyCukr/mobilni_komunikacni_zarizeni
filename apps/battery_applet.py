import tkinter as tk
from PIL import Image, ImageTk
import subprocess
import os


def update_battery_status():
    # This function should read the INA219 data and return the battery percentage
    # For now, we're using a placeholder value. Replace this with your INA219 data reading logic.
    return 50  # Placeholder for battery percentage


def update_icon():
    # Update the battery icon based on the current battery status
    battery_percentage = update_battery_status()

    if battery_percentage > 75:
        img_path = "../images/full-battery.png"  # Replace with your full battery icon path
    elif battery_percentage > 50:
        img_path = "../images/half-battery.png"  # Replace with your half battery icon path
    else:
        img_path = "../images/low-battery.png"   # Replace with your low battery icon path

    img = Image.open(img_path)
    img = img.resize((16, 16), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(img)

    tray_icon.config(image=photo)
    tray_icon.image = photo  # Keep a reference
    root.after(60000, update_icon)  # Update the icon every 60 seconds


root = tk.Tk()
root.withdraw()  # Hide the main window

# Create a system tray icon
img = Image.open("default_battery_icon.png")  # Replace with your default battery icon path
img = img.resize((16, 16), Image.ANTIALIAS)
icon = ImageTk.PhotoImage(img)

tray_icon = tk.Label(root, image=icon)
tray_icon.pack()
tray_icon.after(1000, update_icon)  # Update icon after 1 second to show initial status

# Run the application
root.mainloop()