from tkinter import Toplevel, Text

import customtkinter as ctk
from CTkListbox import CTkListbox
from common.data_manager import DataManager


class ContactsApp(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(fill="both", expand=True)

        master.title("Contacts App")
        master.attributes("-zoomed", True)
        #master.state("zoomed")

        self.contact_data_manager = DataManager('../contacts.json')
        self.contacts = self.contact_data_manager.load_data()

        self.call_history_data_manager = DataManager('../call_history.json')
        self.call_history = self.call_history_data_manager.load_data()

        self.create_contact_listbox()
        self.create_dial_section()

    def create_contact_listbox(self):
        self.contact_listbox = CTkListbox(self, multiple_selection=False, font=("Arial", 32),
                                          command=self.on_contact_select)
        self.contact_listbox.pack(fill="both", expand=True)
        self.show_contacts()

    def show_contacts(self):
        for contact in self.contacts:
            self.contact_listbox.insert("end", f"{contact['name']} ({contact['number']})")

    def on_contact_select(self, contact):
        self.show_call_history(contact)

    def show_call_history(self, contact):
        self.call_history_window = Toplevel(self)
        self.call_history_window.title(f"Call History for {contact}")
        self.call_history_window.attributes("-zoomed", True)

        # Create a frame for the call history text
        text_frame = ctk.CTkFrame(self.call_history_window)
        text_frame.grid(row=0, column=0, sticky="nsew")

        self.call_history_window.grid_rowconfigure(0, weight=1)
        self.call_history_window.grid_columnconfigure(0, weight=1)

        self.call_history_text = Text(text_frame, wrap="word", font=("Arial", 32))
        self.call_history_text.pack(fill="both", expand=True)

        number = contact.split("(")[1][:-1]  # Extract the number from the contact string
        call_history_records = self.call_history.get(number, [])  # Get call history for this number

        for record in call_history_records:
            direction = "Incoming" if record["direction"] == "in" else "Outgoing"
            call_info = f"{record['timestamp']}: {direction}\n"
            self.call_history_text.insert("end", call_info)

        self.call_history_text.configure(state="disabled")

        # Create a frame for the Call button
        button_frame = ctk.CTkFrame(self.call_history_window)
        button_frame.grid(row=1, column=0, sticky="ew")

        self.call_button = ctk.CTkButton(button_frame, text="Call", font=("Arial", 32),
                                         command=lambda: self.dial_contact(contact))
        self.call_button.pack(pady=10)

        # Configure the grid layout so that the text frame expands but the button frame does not
        self.call_history_window.grid_rowconfigure(1, weight=0)

    def dial_contact(self, contact):
        # Implement dialing logic here
        number = contact.split("(")[1][:-1]
        print(f"Dialing {number}")

    def create_dial_section(self):
        self.dial_frame = ctk.CTkFrame(self)
        self.dial_frame.pack(fill="x", padx=5, pady=5)

        self.dial_label = ctk.CTkLabel(self.dial_frame, text="Dial:", font=("Arial", 32))
        self.dial_label.pack(side="left", padx=(5, 0), pady=5)

        self.dial_entry = ctk.CTkEntry(self.dial_frame, font=("Arial", 32))
        self.dial_entry.pack(side="left", fill="x", expand=True, padx=5, pady=5)

        self.dial_button = ctk.CTkButton(self.dial_frame, text="Dial", font=("Arial", 32), command=self.dial_number)
        self.dial_button.pack(side="left", padx=(0, 5), pady=5)

    def dial_number(self):
        # Implement dialing logic here
        number = self.dial_entry.get()
        print(f"Dialing {number}")


if __name__ == "__main__":
    root = ctk.CTk()
    app = ContactsApp(master=root)
    app.mainloop()
