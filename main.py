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

        self.freq = {
            "5s": 5,
            "15s": 15,
            "30s": 30,
            "1m": 60,
            "5m": 300,
            "10m": 600,
            "15m": 900,
            "30m": 1800,
            "1h": 3600,
            "2h": 7200,
        }
        self.key_list = list(self.freq.keys())
        self.val_list = list(self.freq.values())
        self.frequency = tk.StringVar(self)
        self.frq_option = ttk.OptionMenu(self, self.frequency, *self.freq.keys())


        self.parts_list = tk.Listbox(self, height=8, width=60, border=1, background='white')

        self.direct = tk.StringVar()
        self.sto_label = tk.Label(self, textvariable=self.direct)
        self.sto_button = ttk.Button(self, text="Please select the path to direct the returned data", command=self.file_dialog)

        self.status_label = ttk.Label(self, text="Retrieving data")

        self.save_button = ttk.Button(self, text="Save", command=self.add_item)

        self.start_button = ttk.Button(self, text="Start", command=self.start)

        self.stop_button = ttk.Button(self, text="Stop", command=self.stop)

        self.license = ttk.Label(self, text="Bản quyền thuộc về Teslateq Co., Ltd.")
        self.grid_widgets()
        self.get_list()
        self.thread = None

    def create_circle(self, x, y, r, canvasName, **kwargs):
        x0 = x - r
        y0 = y - r
        x1 = x + r
        y1 = y + r
        return canvasName.create_oval(x0, y0, x1, y1, **kwargs)

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

        self.parts_list.grid(row=7, column=0, columnspan=2, rowspan=1, pady=20)
        self.parts_list.bind('<<ListboxSelect>>', self.select_item)

        self.license.grid(row=8, column=0, columnspan=3, sticky='s')

        self.canvas = tk.Canvas(self, width=20, height=20)
        self.canvas.grid(row=6, column=0)
        self.create_circle(10, 10, 9, self.canvas, fill="green")

        self.status_label.grid(row=6, column=0, sticky='e')

    def file_dialog(self):
        filename = filedialog.askdirectory()
        self.direct.set(filename)

    def get_list(self):
        self.parts_list.delete(0, tk.END)
        self.parts_list.insert(tk.END, db.last())
        row = db.last()
        # print(row, row[3])
        self.url_entry.delete(0, tk.END)
        self.url_entry.insert(tk.END, row[1])
        self.token_entry.delete(0, tk.END)
        self.token_entry.insert(tk.END, row[2])
        self.frequency.set(self.key_list[self.val_list.index(row[3])])
        self.direct.set(row[4])
        # print(self.freq[row[3]])

    def add_item(self):
        if self.url_entry.get() == '' or self.token_entry.get() == '':
            messagebox.showerror("Required Fields", " Please fill in all fields.")
            return
        # Insert into DB

        db.insert(self.url_entry.get(), self.token_entry.get(),  self.freq[self.frequency.get()], self.direct.get())
        # Clear list
        self.parts_list.delete(0, tk.END)
        # Insert into list
        self.parts_list.insert(tk.END, (self.url_entry.get(), self.token_entry.get(), self.freq[self.frequency.get()], self.direct.get()))
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
    example.geometry("700x550")
    example.set_theme("breeze")
    example.title('Iotwhynot API Software')
    example.iconphoto(True, PhotoImage(file="image/a.png"))
    example.protocol("WM_DELETE_WINDOW", example.iconify)
    example.mainloop()
