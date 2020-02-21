import os
import sys
import tkinter as tk
from tkinter import ttk, font
from ttkthemes import ThemedTk
from db import Database
from tkinter import messagebox, filedialog
from get_api import GetAPI
from tkinter import *

db = Database('store.db')


class Example(ThemedTk):
    def __init__(self):
        ThemedTk.__init__(self, themebg=True)
        self.url_label = ttk.Label(self, text="Enter request URL")
        self.url_entry = ttk.Entry(self, width=60, textvariable=tk.StringVar())

        self.token_label = ttk.Label(self, text="Authorization")
        self.token_entry = ttk.Entry(self, width=60, textvariable=tk.StringVar())

        self.frq_label = ttk.Label(self, text="Frequency of taking data")

        freq = (
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
        self.frequency = tk.StringVar(self)
        self.frq_option = ttk.OptionMenu(self, self.frequency, *freq)


        self.parts_list = tk.Listbox(self, height=8, width=60, border=1, background='white')

        self.direct = tk.StringVar()
        self.sto_label = tk.Label(self, textvariable=self.direct)
        self.sto_button = ttk.Button(self, text="Please select the path to direct the returned data", command=self.file_dialog)

        self.save_button = ttk.Button(self, text="Save", command=self.add_item)

        self.start_button = ttk.Button(self, text="Start", command=self.start)

        self.stop_button = ttk.Button(self, text="Stop", command=self.stop)

        self.license = ttk.Label(self, text="Bản quyền thuộc về Teslateq Co., Ltd.")
        self.grid_widgets()
        self.get_list()
        self.thread = None


    def grid_widgets(self):
        """Put widgets in the grid"""
        sticky = {"sticky": "nswe"}
        self.url_label.grid(row=0, column=0, padx=20, pady=20, **sticky)
        self.url_entry.grid(row=0, column=1, sticky='we')

        self.token_label.grid(row=1, column=0, padx=20, pady=20, **sticky)
        self.token_entry.grid(row=1, column=1, sticky='we')

        self.frq_label.grid(row=2, column=0, padx=20, pady=20, **sticky)
        self.frq_option.grid(row=2, column=1, sticky='we')

        self.sto_button.grid(row=3, column=0, columnspan=3, padx=20, pady=15, sticky='w')
        self.sto_label.grid(row=4, column=0, padx=20, columnspan=3, sticky='w')

        self.start_button.grid(row=5, column=1, pady=15, sticky='w')
        self.stop_button.grid(row=5, column=1)
        self.save_button.grid(row=5, column=1, sticky='e')

        self.parts_list.grid(row=6, column=0, columnspan=2, rowspan=2, pady=20)
        self.parts_list.bind('<<ListboxSelect>>', self.select_item)

        self.license.grid(row=7, column=0, columnspan=3, sticky='s')

    def file_dialog(self):
        filename = filedialog.askdirectory()
        self.direct.set(filename)

    def get_list(self):
        self.parts_list.delete(0, tk.END)
        self.parts_list.insert(tk.END, db.last())

    def add_item(self):
        if self.url_entry.get() == '' or self.token_entry.get() == '':
            messagebox.showerror("Required Fields", " Please fill in all fields.")
            return
        # Insert into DB
        db.insert(self.url_entry.get(), self.token_entry.get(), self.frequency.get(), self.direct.get())
        # Clear list
        self.parts_list.delete(0, tk.END)
        # Insert into list
        self.parts_list.insert(tk.END, (self.url_entry.get(), self.token_entry.get(), self.frequency.get(), self.direct.get()))

        self.get_list()


    def select_item(self, event):
        # # Create global selected item to use in other functions
        # global self.selected_item
        try:
            index = self.parts_list.curselection()[0]
            # Get selected item
            self.selected_item = self.parts_list.get(index)
            # Add text to entries
            self.url_entry.delete(0, tk.END)
            self.url_entry.insert(tk.END, self.selected_item[1])
            self.token_entry.delete(0, tk.END)
            self.token_entry.insert(tk.END, self.selected_item[2])
            self.frequency.set(self.selected_item[3])
            self.direct.set(self.selected_item[4])
        except IndexError:
            pass

    def start(self):
        if self.url_entry.get() == '' or self.token_entry.get() == '':
            messagebox.showerror(
                "Required Fields", " Please fill in all fields.")
            return

        self.thread = GetAPI(
            url=self.url_entry.get(),
            token=self.token_entry.get(),
            freq=self.frequency.get(),
            direct=self.direct.get(),
        )
        self.thread.start()
        print("Started", self.thread)

    def stop(self):
        if self.thread:
            self.thread.stop()
        self.destroy()


if __name__ == '__main__':
    example = Example()
    example.geometry("700x350+300+300")
    example.set_theme("breeze")
    example.title('Iotwhynot API Software')
    example.iconphoto(True, PhotoImage(file="image/a.png"))
    example.mainloop()
