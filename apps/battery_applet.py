import os
import random
import threading
import time

from pystray import MenuItem as item
from pystray import Menu as menu
import pystray
from PIL import Image
import tkinter as tk

window = tk.Tk()
window.title("Battery status")

script_path = os.path.dirname(os.path.realpath(__file__))

full_battery_image = Image.open(os.path.join(script_path, "../images/full-battery.png"))
half_battery_image = Image.open(os.path.join(script_path, "../images/half-battery.png"))
low_battery_image = Image.open(os.path.join(script_path, "../images/low-battery.png"))
battery_image = Image.open(os.path.join(script_path, "../images/battery.png"))


def get_battery_percentage():
    # Replace this with actual code to get battery percentage
    return random.randint(0, 100)


def update_battery_percentage(icon):
    while True:

        try:
            battery_percentage = get_battery_percentage()

            print(f"Battery percentage: {battery_percentage}")

            icon.menu = menu(item(f'Battery: {battery_percentage}%', lambda: None))

            # Update icon image based on battery percentage
            if battery_percentage > 90:
                icon.icon = full_battery_image
            elif battery_percentage > 75:
                icon.icon = battery_image
            elif battery_percentage > 40:
                icon.icon = half_battery_image
            else:
                icon.icon = low_battery_image

            icon.update_menu()

            time.sleep(5)  # Update every 5 second
        except Exception as e:
            print(e)


def withdraw_window():
    window.withdraw()
    image = Image.open("../images/battery.png")
    menu_item = item(f"Battery: {get_battery_percentage()}%", lambda: None)
    icon = pystray.Icon("name", image, "title", menu(menu_item))

    # Start a thread to update the battery percentage
    tooltip_thread = threading.Thread(target=update_battery_percentage, args=(icon,))
    tooltip_thread.start()

    icon.run()

withdraw_window()
window.mainloop()


