import os
import sys
if sys.version_info.major == 3:
    import tkinter as tk
    from tkinter import ttk, font
else:
    import Tkinter as tk
    import ttk
from ttkthemes import ThemedTk
from db import Database
from tkinter import messagebox, filedialog
from get_api import GetAPI


db = Database('store.db')

from tkinter import *

class Example(ThemedTk):
    """
    Example that is used to create screenshots for new themes.
    """
    def __init__(self):
        ThemedTk.__init__(self, themebg=True)
        self.url_label = ttk.Label(self, text="Enter request URL")
        self.url_entry = ttk.Entry(self, width=60, textvariable=tk.StringVar())

        self.token_label = ttk.Label(self, text="Authorization")
        self.token_entry = ttk.Entry(self, width=60, textvariable=tk.StringVar())

        self.frq_label = ttk.Label(self, text="Frequency of taking data")

        baudrates = (
            9600,
            19200,
            38400,
            57600,
            115200,
            128000,
            256000,
            500000,
            512000,
        )
        self.baudrate = tk.StringVar(self)
        self.frq_option = ttk.OptionMenu(self, self.baudrate, *baudrates)

        self.abc = ttk.Label(self, text="Bản quyền thuộc về Teslateq Co., Ltd.")
        self.parts_list = tk.Listbox(self, height=8, width=60, border=1, background='white')

        self.sto_label = ttk.Label(self, text="Data storage place")
        self.sto_entry = ttk.Entry(self, width=30, textvariable=tk.StringVar())
        self.sto_button = ttk.Button(self, text="Select the storage directory", command=self.file_dialog)

        self.save_button = ttk.Button(self, text="Save", command=self.add_item)

        self.start_button = ttk.Button(self, text="Start", command=self.start)

        self.stop_button = ttk.Button(self, text="Stop", command=self.stop)

        self.grid_widgets()
        self.get_list()
        self.thread = None


    def grid_widgets(self):
        """Put widgets in the grid"""
        sticky = {"sticky": "nswe"}
        self.url_label.grid(row=0, column=0, padx=20, pady=20, **sticky)
        self.url_entry.grid(row=0, column=1, sticky='we')
        # self.abc.grid()
        self.token_label.grid(row=1, column=0, padx=20, pady=20, **sticky)
        self.token_entry.grid(row=1, column=1, sticky='we')

        self.frq_label.grid(row=2, column=0, padx=20, pady=20, **sticky)
        self.frq_option.grid(row=2, column=1, sticky='we')

        self.sto_label.grid(row=3, column=0, padx=20, pady=20, **sticky)
        self.sto_entry.grid(row=3, column=1, sticky='w')
        self.sto_button.grid(row=3, column=1, sticky='e')


        self.start_button.grid(row=4, column=1, sticky='w')
        self.stop_button.grid(row=4, column=1)
        self.save_button.grid(row=4, column=1, sticky='e')

        self.parts_list.grid(row=5, column=0, columnspan=2, rowspan=2, pady=20)
        self.parts_list.bind('<<ListboxSelect>>', self.select_item)

    def file_dialog(self):
        filename = filedialog.askdirectory()
        self.sto_entry.delete(0, END)
        self.sto_entry.insert(END, filename)
        print(filename)

    def get_list(self):
        self.parts_list.delete(0, tk.END)
        self.parts_list.insert(tk.END, db.last())
        a = db.lasts()
        print(a)


    def add_item(self):
        if self.url_entry.get() == '' or self.token_entry.get() == '':
            messagebox.showerror("Required Fields", " Please fill in all fields.")
            return
        # Insert into DB
        print(self.url_entry.get(), self.token_entry.get(), self.baudrate.get(), self.sto_entry.get())
        db.insert(self.url_entry.get(), self.token_entry.get(), self.baudrate.get(), self.sto_entry.get())
        # Clear list
        self.parts_list.delete(0, tk.END)
        # Insert into list
        self.parts_list.insert(tk.END, (self.url_entry.get(), self.token_entry.get(), self.baudrate.get(), self.sto_entry.get()))

        self.get_list()


    def select_item(self, event):
        # # Create global selected item to use in other functions
        # global self.selected_item

        try:
            # Get index
            index = self.parts_list.curselection()[0]
            # Get selected item
            self.selected_item = self.parts_list.get(index)
            # print(selected_item) # Print tuple
            print(index, self.selected_item)
            # Add text to entries
            self.url_entry.delete(0, tk.END)
            self.url_entry.insert(tk.END, self.selected_item[1])
            self.token_entry.delete(0, tk.END)
            self.token_entry.insert(tk.END, self.selected_item[2])
            self.baudrate.set(self.selected_item[3])
            self.sto_entry.delete(0, tk.END)
            self.sto_entry.insert(tk.END, self.selected_item[4])

        except IndexError:
            pass

    def start(self):
        if self.part_text.get() == '' or self.customer_text.get() == '':
            messagebox.showerror(
                "Required Fields", " Please fill in all fields.")
            return

        self.thread = GetAPI(
            url=self.part_text.get(),
            token=self.customer_text.get(),
        )
        self.thread.start()
        print('Start!')
        self.populate_list()

    def stop(self):
        if self.thread:
            self.thread.stop()
        self.destroy()


if __name__ == '__main__':
    example = Example()
    example.geometry("700x300+300+300")
    example.set_theme("breeze")
    example.title('Iotwhynot API Software')
    example.iconphoto(True, PhotoImage(file="image/a.png"))
    example.mainloop()
