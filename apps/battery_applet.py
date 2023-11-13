import random
import threading
import time

from pystray import MenuItem as item, Icon, Menu as menu
from PIL import Image
import tkinter as tk

def get_battery_percentage():
    # Replace this with actual code to get battery percentage
    return random.randint(0, 100)

def create_icon(battery_percentage):
    icon_image = get_battery_icon_image(battery_percentage)
    menu_items = menu(item(f'Battery: {battery_percentage}%', lambda: None))
    icon = Icon("battery_icon", icon_image, menu=menu_items)
    icon.run()

def get_battery_icon_image(battery_percentage):
    if battery_percentage > 90:
        return Image.open("../images/full-battery.png")
    elif battery_percentage > 75:
        return Image.open("../images/battery.png")
    elif battery_percentage > 40:
        return Image.open("../images/half-battery.png")
    else:
        return Image.open("../images/low-battery.png")

def update_icon():
    while True:
        battery_percentage = get_battery_percentage()

        print(f"Battery percentage: {battery_percentage}")

        icon.stop()

        create_icon(battery_percentage)
        time.sleep(5)  # Update every 5 seconds

window = tk.Tk()
window.title("Battery status")

# Initial icon creation
battery_percentage = get_battery_percentage()
icon = Icon("battery_icon", get_battery_icon_image(battery_percentage), menu=menu(item(f'Battery: {battery_percentage}%', lambda: None)))

icon_thread = threading.Thread(target=update_icon)
icon_thread.daemon = True  # Set as a daemon so it ends with the main program
icon_thread.start()

window.withdraw()
window.mainloop()
