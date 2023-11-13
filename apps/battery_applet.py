import random
import threading
import time

from pystray import MenuItem as item
import pystray
from PIL import Image
import tkinter as tk

window = tk.Tk()
window.title("Battery status")


def get_battery_percentage():
    # Replace this with actual code to get battery percentage
    return random.randint(0, 100)


def update_battery_percentage(menu_item, icon):
    battery_percentage = get_battery_percentage()
    menu_item.text = f"Battery: {battery_percentage}%"

    # Update icon image based on battery percentage
    if battery_percentage > 75:
        icon.icon = Image.open("battery_full.png")
    elif battery_percentage > 40:
        icon.icon = Image.open("battery_half.png")
    else:
        icon.icon = Image.open("battery_low.png")

    icon.update_menu()

    time.sleep(5)  # Update every 60 seconds


def withdraw_window():
    window.withdraw()
    image = Image.open("../images/battery.png")
    menu_item = item(f"Battery: {get_battery_percentage()}%", lambda: None)
    menu = (menu_item,)
    icon = pystray.Icon("name", image, "title", menu)

    # Start a thread to update the battery percentage
    tooltip_thread = threading.Thread(target=update_battery_percentage, args=(menu_item, icon))
    tooltip_thread.start()

    icon.run()

withdraw_window()
window.mainloop()


