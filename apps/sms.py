import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext
import serial
import time

# Constants for serial communication
SERIAL_PORT = '/dev/ttyUSB2'  # Update this based on your setup
BAUD_RATE = 115200

# Initialize serial communication with the SIM8202G-M2 module
def init_serial():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        return ser
    except Exception as e:
        messagebox.showerror("Serial Connection Error", str(e))
        return None

# Function to send AT commands and read responses
def send_at_command(ser, command):
    try:
        ser.write((command + '\r\n').encode())
        time.sleep(1)
        response = ser.read(ser.inWaiting()).decode()
        return response
    except Exception as e:
        messagebox.showerror("AT Command Error", str(e))
        return None

# Function to send an SMS
def send_sms(phone_number: int, message: str):
    send_at_command(ser, 'AT+CMGF=1')  # Set SMS text mode
    send_at_command(ser, f'AT+CMGS="{phone_number}"')
    send_at_command(ser, message + chr(26))  # Message followed by CTRL+Z
    messagebox.showinfo("SMS Sent", "SMS sent successfully!")

# Function to read SMS
def read_sms():
    send_at_command(ser, 'AT+CMGF=1')  # Set SMS text mode
    messages = send_at_command(ser, 'AT+CMGL="ALL"')  # List all SMS
    sms_display.delete(1.0, tk.END)
    sms_display.insert(tk.END, messages)

# GUI setup
def setup_gui(root, ser):
    global sms_display

    root.title("Raspberry Pi SMS App")

    send_sms_button = tk.Button(root, text="Send SMS", command=send_sms)
    send_sms_button.grid(row=0, column=0, padx=10, pady=10)

    read_sms_button = tk.Button(root, text="Read SMS", command=read_sms)
    read_sms_button.grid(row=0, column=1, padx=10, pady=10)

    sms_display = scrolledtext.ScrolledText(root, width=40, height=10)
    sms_display.grid(row=1, column=0, columnspan=2, padx=10, pady=10)


global ser, root
ser = init_serial()
if ser:
    print("Serial communication initialized.")
else:
    print("Failed to initialize serial communication.")


# Main function
def main():
    if ser:
        root = tk.Tk()
        setup_gui(root, ser)
        root.mainloop()
    else:
        print("Failed to initialize serial communication.")


if __name__ == "__main__":
    main()

