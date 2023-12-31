#!/usr/bin/env python3
import os

os.environ['DISPLAY'] = ':0.0'

import random
import threading
import time
from time import sleep

sleep(30)

from pystray import MenuItem as item
from pystray import Menu as menu
import pystray
from PIL import Image
import tkinter as tk


from INA219 import INA219

window = tk.Tk()
window.title("Battery status")

images_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "images")

full_battery_image = Image.open(os.path.join(images_directory, "full-battery.png"))
half_battery_image = Image.open(os.path.join(images_directory, "half-battery.png"))
low_battery_image = Image.open(os.path.join(images_directory, "low-battery.png"))
battery_image = Image.open(os.path.join(images_directory, "battery.png"))

ina219 = INA219(addr=0x42)


def get_battery_percentage() -> float:

    bus_voltage = ina219.getBusVoltage_V()  # voltage on V- (load side)
    percent = (bus_voltage - 6) / 2.4 * 100
    if (percent > 100): percent = 100
    if (percent < 0): percent = 0

    # return percent with one decimal place
    return round(percent, 1)


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
    image = Image.open(os.path.join(images_directory, "battery.png"))
    menu_item = item(f"Battery: {get_battery_percentage()}%", lambda: None)
    icon = pystray.Icon("name", image, "title", menu(menu_item))

    # Start a thread to update the battery percentage
    tooltip_thread = threading.Thread(target=update_battery_percentage, args=(icon,))
    tooltip_thread.start()

    icon.run()

withdraw_window()
window.mainloop()


