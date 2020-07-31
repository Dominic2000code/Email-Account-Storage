# from tkinter import *
import tkinter as tk
from tkinter import messagebox
from db import Database

# Created by SidCorp
db = Database('store.sqlite')


class PopUpWindow:
    loop = False
    attempts = 0

    def __init__(self, master):
        topLevel = self.topLevel = tk.Toplevel(master)
        topLevel.title("Input Password")
        topLevel.iconbitmap(r"C:\Users\Dominic\Pictures\New folder\key_password_lock_800.ico")
        topLevel.geometry("250x100")
        topLevel.resizable(width=False, height=False)
        self.label = tk.Label(topLevel, text="Password: ", font=('Courier', 14), justify=tk.CENTER)
        self.label.pack()
        self.entry = tk.Entry(topLevel, show="*", width=30)
        self.entry.pack(pady=10)
        self.button = tk.Button(topLevel, text="Submit", command=self.onClick, font=('Courier', 14))
        self.button.pack()

    def onClick(self):
        value = self.entry.get()
        password = 'root'

        if value == password:
            self.loop = True
            self.topLevel.destroy()
            root.deiconify()
        else:
            self.attempts += 1
            if self.attempts == 5:
                root.quit()
            self.entry.delete(0, tk.END)
            messagebox.showerror("Incorrect Password",
                                 "Incorrect password, you have " + str(5 - self.attempts) + " remaining ")


class Application(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        master.geometry("500x350")
        self.createWidgets()
        self.selected_items = 0
        self.populate_list()

    def createWidgets(self):
        self.entity_label = tk.Label(self.master, text="Add Account", font=('Courier', 18))
        self.entity_label.grid(columnspan=3, row=0)

        # Name field
        self.name_text = tk.StringVar()
        self.name_label = tk.Label(self.master, text="Name: ", font=('Courier', 14))
        self.name_entry = tk.Entry(self.master, textvariable=self.name_text, font=('Courier', 14))
        self.name_label.grid(row=1, sticky=tk.E, padx=3)
        self.name_entry.grid(columnspan=3, row=1, column=1, padx=2, sticky=tk.W)

        # Email field
        self.email_text = tk.StringVar()
        self.email_label = tk.Label(self.master, text="Email: ", font=('Courier', 14))
        self.email_entry = tk.Entry(self.master, textvariable=self.email_text, font=('Courier', 14))
        self.email_label.grid(row=2, sticky=tk.E, padx=3)
        self.email_entry.grid(columnspan=3, row=2, column=1, padx=2, sticky=tk.W)

        # Password field
        self.password_text = tk.StringVar()
        self.password_label = tk.Label(self.master, text="Password: ", font=('Courier', 14))
        self.password_entry = tk.Entry(self.master, show='*',textvariable=self.password_text, font=('Courier', 14))
        self.password_label.grid(row=3, sticky=tk.E, padx=3)
        self.password_entry.grid(columnspan=3, row=3, column=1, padx=2, sticky=tk.W)

        # Accounts list (listbox)
        self.accounts_list = tk.Listbox(self.master, height=8, width=55)
        self.accounts_list.grid(row=5, column=0, columnspan=3, rowspan=6, pady=20, padx=20)

        # Vertical scrollbar
        self.scrollbar = tk.Scrollbar(self.master)
        self.scrollbar.grid(row=5, column=3)

        # Horizontal scrollBar
        self.hscrollbar = tk.Scrollbar(self.master, orient=tk.HORIZONTAL)
        self.hscrollbar.grid(row=6, column=3)

        # Set scrollbar to accounts
        self.accounts_list.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.accounts_list.yview)

        self.accounts_list.configure(xscrollcommand=self.hscrollbar.set)
        self.hscrollbar.configure(command=self.accounts_list.xview)

        # Bind select
        self.accounts_list.bind('<<ListboxSelect>>', self.select_item)

        # Buttons
        self.add_button = tk.Button(self.master, text="Add Account", width=12, command=self.add_item)
        self.add_button.grid(row=4, column=0, pady=20)

        self.remove_button = tk.Button(self.master, text="Remove Account", width=13, command=self.remove_item)
        self.remove_button.grid(row=4, column=1, pady=20)

        self.update_button = tk.Button(self.master, text="Update Account", width=13, command=self.update_item)
        self.update_button.grid(row=4, column=2, pady=20)

        self.clear_button = tk.Button(self.master, text="Clear Text", width=12, command=self.clear_text)
        self.clear_button.grid(row=4, column=3, pady=20)

    def populate_list(self):
        self.accounts_list.delete(0, tk.END)
        for row in db.fetch():
            if row == int():
                continue
            self.accounts_list.insert(tk.END, row)

    def add_item(self):
        if self.name_text.get() == "" or self.email_text.get() == "" or self.password_text == "":
            messagebox.showerror("Required Fields", "Please include all fields")
            return

        else:
            # Insert into DB
            db.insert(self.name_text.get(), self.email_text.get(), self.password_text.get())
            # Clear list
            self.accounts_list.delete(0, tk.END)
            # Insert into list
            self.accounts_list.insert(tk.END, (self.name_text.get(), self.email_text.get(), self.password_text.get()))
            self.clear_text()
            self.populate_list()

    def select_item(self, event):
        try:
            # Get index
            index = self.accounts_list.curselection()[0]
            # Get selected item
            self.selected_item = self.accounts_list.get(index)

            # Add text to entries
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(tk.END, self.selected_item[1])
            self.email_entry.delete(0, tk.END)
            self.email_entry.insert(tk.END, self.selected_item[2])
            self.password_entry.delete(0, tk.END)
            self.password_entry.insert(tk.END, self.selected_item[3])
        except IndexError:
            pass

    def remove_item(self):
        db.remove(self.selected_item[0])
        self.clear_text()
        self.populate_list()

    def update_item(self):
        db.update(self.selected_item[0], self.name_text.get(), self.email_text.get(), self.password_text.get())
        self.populate_list()

    def clear_text(self):
        self.name_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)


root = tk.Tk()
root.withdraw()
root.title("Email Storage          DesignedBy@SidCorp")
root.iconbitmap(r"C:\Users\Dominic\Pictures\New folder\key_password_lock_800.ico")
app = Application(root)
popup = PopUpWindow(root)

root.mainloop()
