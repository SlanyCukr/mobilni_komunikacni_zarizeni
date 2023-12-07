from datetime import datetime
import customtkinter as ctk
from tkinter import Toplevel, scrolledtext, Entry, Button, simpledialog
from CTkListbox import CTkListbox

from common.data_manager import DataManager

from sms import send_sms


class MessagingApp(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(fill="both", expand=True)

        master.title("Messaging App")
        master.attributes("-zoomed", True)
        #master.state("zoomed")

        self.message_data_manager = DataManager('../messages.json')
        self.contact_data_manager = DataManager('../contacts.json')

        self.message_history = self.message_data_manager.load_data()
        self.contacts = self.contact_data_manager.load_data()

        self.create_contact_message_listbox()

    def open_new_message_window(self):
        # Ask for the contact number to which the user wants to send a message
        contact_number = simpledialog.askstring("New Message", "Enter Contact Number:")
        if contact_number:
            self.display_message_window(contact_number)

    def create_contact_message_listbox(self):
        # Create a frame to contain the listbox and the new message button
        self.listbox_frame = ctk.CTkFrame(self)
        self.listbox_frame.pack(side="left", fill="both", expand=True)

        # Create the listbox for contact messages inside the frame
        self.contact_message_listbox = CTkListbox(
            self.listbox_frame,
            multiple_selection=False,
            font=("Arial", 32),
            command=self.on_contact_select,
        )
        self.contact_message_listbox.pack(fill="both", expand=True)
        self.contact_message_listbox.bind("<<ListboxSelect>>", self.on_contact_select)

        # Show existing contacts in the listbox
        self.show_contacts()

        # New Button to open a window to send a new message, placed below the listbox inside the frame
        self.new_message_button = Button(self.listbox_frame, text="New Message", font=("Arial", 16),
                                         command=self.open_new_message_window)
        self.new_message_button.pack(pady=10)

    def show_contacts(self):
        try:
            self.contact_message_listbox.delete(0, "end")
            self.contact_message_listbox.delete(1, "end")
        except:
            pass

        for contact in self.contacts:
            self.contact_message_listbox.insert("end", contact['name'])

        for number, messages in self.message_history.items():
            if number not in [contact['number'] for contact in self.contacts]:
                self.contact_message_listbox.insert("end", number)

    def on_contact_select(self, event):
        selection_index = self.contact_message_listbox.curselection()
        if selection_index == ():
            return
        selected_contact = self.contact_message_listbox.get(selection_index)
        self.display_message_window(selected_contact)

    def display_message(self, selected_contact) -> int:
        """
        Display message history for selected contact
        :param selected_contact: Contact name
        :return: Contact number
        """
        self.chat_area.delete('1.0', 'end')

        # find contact number in contacts one liner
        try:
            contact_number = next(contact['number'] for contact in self.contacts if contact['name'] == selected_contact)
        except StopIteration:
            contact_number = selected_contact
        messages = self.message_history.get(selected_contact,
                                            []) if selected_contact in self.contacts else self.message_history.get(
            contact_number, [])

        for message in messages:
            direction = message['direction']
            text = message['message']
            timestamp = message['timestamp']
            formatted_message = f"{timestamp} - {direction}: {text}\n"
            self.chat_area.insert("end", formatted_message)

        return contact_number

    def display_message_window(self, selected_contact: str):
        """
        Display a window to send and receive messages
        :param selected_contact: Contact name
        """
        self.new_window = Toplevel(self)
        self.new_window.title(f"Chat with {selected_contact}")
        self.new_window.attributes("-zoomed", True)

        self.chat_area = scrolledtext.ScrolledText(self.new_window, font=("Arial", 16))
        self.chat_area.pack(fill="both", expand=True, padx=5, pady=5)

        self.message_entry = Entry(self.new_window, font=("Arial", 16))
        self.message_entry.pack(fill="x", expand=False, padx=5, pady=5)

        contact_number = self.display_message(selected_contact)

        self.send_button = Button(self.new_window, text="Send", font=("Arial", 16), command=lambda: self.send_message(contact_number, selected_contact))
        self.send_button.pack(padx=5, pady=5)

        self.back_button = Button(self.new_window, text="Back", font=("Arial", 16), command=self.new_window.destroy)
        self.back_button.pack(padx=5, pady=5)

    def send_message(self, contact_number: int, selected_contact: str):
        text_to_send = self.message_entry.get()

        print(f"Sending text {text_to_send} to {contact_number}.")

        # send message using AT commands
        send_sms(contact_number, text_to_send)

        if contact_number not in self.message_history:
            self.message_history[contact_number] = []

        self.message_history[contact_number].append({
            'direction': 'out',
            'message': text_to_send,
            'timestamp': datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),  # timestamp in the form 2023-10-28T11:00:00
        })

        self.message_data_manager.save_data(self.message_history)

        # update message window
        self.display_message(selected_contact)

        # update main contact listbox
        self.show_contacts()


if __name__ == "__main__":
    root = ctk.CTk()
    app = MessagingApp(master=root)
    app.mainloop()
