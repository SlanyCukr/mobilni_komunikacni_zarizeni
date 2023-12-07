import tkinter as tk
from tkinter import messagebox
import serial
import time

# Constants for serial communication
SERIAL_PORT = '/dev/ttyUSB2'
BAUD_RATE = 115200
BUTTON_WIDTH = 10
BUTTON_HEIGHT = 3
FONT_SIZE = 18

# Global variables
call_history = []

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

# Function to make a call
def make_call(phone_number):
    if phone_number:
        response = send_at_command(ser, f'ATD{phone_number};')
        if response:
            messagebox.showinfo("Call", f"Calling {phone_number}...")
            call_history.append(f"Outgoing call to {phone_number}")
            update_call_history_display()
        else:
            messagebox.showerror("Call Error", "Failed to make the call.")

def hang_up():
    response = send_at_command(ser, 'ATH')
    if response:
        messagebox.showinfo("Hang Up", "Call ended.")
        call_history.append("Call ended")
        update_call_history_display()
    else:
        messagebox.showerror("Error", "Failed to hang up the call.")

def check_for_incoming_calls():
    response = send_at_command(ser, 'AT+CLCC')
    if response and "+CLCC: 1,1" in response:
        if messagebox.askyesno("Incoming Call", "Answer the call?"):
            send_at_command(ser, 'ATA')
            call_history.append("Incoming call answered")
            update_call_history_display()
        else:
            hang_up()
    root.after(5000, check_for_incoming_calls)

# GUI setup
def setup_gui(root, ser):
    global dialed_number_entry, call_history_text

    root.title("Raspberry Pi Phone App")
    root.geometry('600x800')

    dialed_number_entry = tk.Entry(root, font=('Helvetica', FONT_SIZE))
    dialed_number_entry.grid(row=0, column=0, columnspan=3, padx=20, pady=20)

    # Number pad
    numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '*', '0', '#']
    for i, number in enumerate(numbers):
        button = tk.Button(root, text=number, width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                           font=('Helvetica', FONT_SIZE),
                           command=lambda num=number: dialed_number_entry.insert(tk.END, num))
        button.grid(row=i // 3 + 1, column=i % 3, padx=10, pady=10)

    # Clear, Call, and Hang Up buttons
    clear_button = tk.Button(root, text='Clear', width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                             font=('Helvetica', FONT_SIZE),
                             command=lambda: dialed_number_entry.delete(0, tk.END))
    clear_button.grid(row=5, column=0, padx=10, pady=10)

    call_button = tk.Button(root, text="Call", width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                            font=('Helvetica', FONT_SIZE),
                            command=lambda: make_call(dialed_number_entry.get()))
    call_button.grid(row=5, column=1, padx=10, pady=10)

    hang_up_button = tk.Button(root, text="Hang Up", width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                               font=('Helvetica', FONT_SIZE), command=hang_up)
    hang_up_button.grid(row=5, column=2, padx=10, pady=10)

    # Call History Display
    call_history_label = tk.Label(root, text="Call History", font=('Helvetica', FONT_SIZE))
    call_history_label.grid(row=6, column=0, columnspan=3, pady=(10,0))

    call_history_text = tk.Text(root, height=10, width=30)
    call_history_text.grid(row=7, column=0, columnspan=3, padx=20, pady=10)

# Function to update call history in the GUI
def update_call_history_display():
    call_history_text.delete('1.0', tk.END)
    for entry in call_history:
        call_history_text.insert(tk.END, entry + '\n')

# Main function
def main():
    global ser, root
    ser = init_serial()
    if ser:
        root = tk.Tk()
        setup_gui(root, ser)
        root.after(5000, check_for_incoming_calls)
        root.mainloop()
    else:
        print("Failed to initialize serial communication.")

if __name__ == "__main__":
    main()
