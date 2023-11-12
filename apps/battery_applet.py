import tkinter as tk
from PIL import Image, ImageTk
import os


def update_battery_info():
    # Read battery information
    # Update the icon and percentage
    root.after(60000, update_battery_info)  # Update every minute

root = tk.Tk()
root.overrideredirect(True)  # Hide the window border
root.geometry("+X+Y")  # Replace X and Y with the coordinates for the top right corner

# Load your battery icon
img = Image.open("../images/battery.png")
imgTk = ImageTk.PhotoImage(img)

label = tk.Label(root, image=imgTk)
label.pack()

update_battery_info()
root.mainloop()
