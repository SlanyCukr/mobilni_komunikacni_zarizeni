import customtkinter as ctk
from tkinter import Toplevel, scrolledtext, Entry, Button
from CTkListbox import CTkListbox
from common.data_manager import DataManager


class MessagingApp(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(fill="both", expand=True)

        master.title("Messaging App")
        master.attributes("-zoomed", True)
        #master.state("zoomed")

        self.message_data_manager = DataManager('messages.json')
        self.contact_data_manager = DataManager('contacts.json')

        self.message_history = self.message_data_manager.load_data()
        self.contacts = self.contact_data_manager.load_data()

        self.create_contact_message_listbox()

    def create_contact_message_listbox(self):
        self.contact_message_listbox = CTkListbox(
            self,
            multiple_selection=False,
            font=("Arial", 32),
            command=self.on_contact_select,
        )
        self.contact_message_listbox.pack(side="left", fill="both", expand=True)
        self.contact_message_listbox.bind("<<ListboxSelect>>", self.on_contact_select)

        self.show_contacts()

    def show_contacts(self):
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
        self.display_messages(selected_contact)

    def display_messages(self, selected_contact):
        self.new_window = Toplevel(self)
        self.new_window.title(f"Chat with {selected_contact}")
        self.new_window.attributes("-zoomed", True)

        self.chat_area = scrolledtext.ScrolledText(self.new_window, font=("Arial", 16))
        self.chat_area.pack(fill="both", expand=True, padx=5, pady=5)

        self.message_entry = Entry(self.new_window, font=("Arial", 16))
        self.message_entry.pack(fill="x", expand=False, padx=5, pady=5)

        self.send_button = Button(self.new_window, text="Send", font=("Arial", 16), command=self.send_message)
        self.send_button.pack(padx=5, pady=5)

        self.back_button = Button(self.new_window, text="Back", font=("Arial", 16), command=self.new_window.destroy)
        self.back_button.pack(padx=5, pady=5)

        # find contact number in contacts one liner
        try:
            contact_number = next(contact['number'] for contact in self.contacts if contact['name'] == selected_contact)
        except StopIteration:
            contact_number = selected_contact
        messages = self.message_history.get(selected_contact, []) if selected_contact in self.contacts else self.message_history.get(contact_number, [])

        for message in messages:
            direction = message['direction']
            text = message['message']
            timestamp = message['timestamp']
            formatted_message = f"{timestamp} - {direction}: {text}\n"
            self.chat_area.insert("end", formatted_message)

    def send_message(self):
        # Implement sending message logic
        pass


if __name__ == "__main__":
    root = ctk.CTk()
    app = MessagingApp(master=root)
    app.mainloop()
