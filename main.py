import os
import sys
import getpass
import tkinter as tk
from tkinter import ttk, font
from ttkthemes import ThemedTk
from db import Database
from tkinter import messagebox, filedialog
from ttkwidgets.autocomplete import AutocompleteCombobox
from get_api import GetAPI
from tkinter import *

db = Database('store.db')


class Example(ThemedTk):
    def __init__(self):
        ThemedTk.__init__(self, themebg=True)
        self.url_label = ttk.Label(self, text="Enter request URL")
        self.url_entry =  AutocompleteCombobox(self, completevalues=["https://iotwhynot.com/chip_manager/read_data_api"])

        self.token_label = ttk.Label(self, text="Authorization")
        self.token_entry = ttk.Entry(self, width=50, textvariable=tk.StringVar())
        self.frq_label = ttk.Label(self, text="Frequency of taking data")

        self.freq = {
            '5s': 5,
            ' 5s': 5,
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
        print(*self.freq.keys())
        self.frq_option = ttk.OptionMenu(self, self.frequency, *self.freq.keys())

        self.parts_list = tk.Listbox(self, height=8, width=50, border=1, background='white')

        self.auto = tk.BooleanVar(value=True)
        self.checked = ttk.Checkbutton(self, text="Automatically start the software with windows", variable=self.auto)

        self.direct = tk.StringVar()
        self.sto_label = tk.Label(self, textvariable=self.direct)
        self.sto_button = ttk.Button(self, text="Please select the path to direct the returned data", command=self.file_dialog)

        # self.save_button = ttk.Button(self, text="Save", command=self.add_item)
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

        self.checked.grid(row=3, columnspan=2,padx=20, sticky='w')

        self.sto_button.grid(row=4, column=0, columnspan=3, padx=20, pady=15, sticky='w')
        self.sto_label.grid(row=5, column=0, padx=20, columnspan=3, sticky='w')

        self.start_button.grid(row=6, column=1, pady=15, sticky='w')
        self.stop_button.grid(row=6, column=1, pady=15, sticky='sn')
        # self.save_button.grid(row=6, column=1, sticky='e')

        self.license.grid(row=8, column=0, columnspan=3, sticky='s')

    def file_dialog(self):
        filename = filedialog.askdirectory()
        self.direct.set(filename)

    def get_list(self):
        row = db.last()
        print(row)
        if row:
            self.url_entry.delete(0, tk.END)
            self.url_entry.insert(tk.END, row[1])
            self.token_entry.delete(0, tk.END)
            self.token_entry.insert(tk.END, row[2])
            self.frequency.set(self.key_list[self.val_list.index(row[3])])
            self.direct.set(row[4])
            self.auto.set(row[5])

    def add_item(self):
        print(self.auto.get())
        direct = self.direct.get()
        if not direct:
            dirName = 'downloads'
            if not os.path.exists(dirName):
                os.mkdir(dirName)
            direct = os.getcwd() + '/' + dirName
        print(direct)
        db.insert(self.url_entry.get(), self.token_entry.get(),  self.freq[self.frequency.get()], direct,  self.auto.get())
        # Clear list
        # self.parts_list.delete(0, tk.END)
        # Insert into list
        # self.parts_list.insert(tk.END, (self.url_entry.get(), self.token_entry.get(), self.freq[self.frequency.get()], self.direct.get(), self.auto.get()))
        self.get_list()


    def select_item(self, event):
        try:
            index = self.parts_list.curselection()[0]
            self.selected_item = self.parts_list.get(index)
            self.url_entry.delete(0, tk.END)
            self.url_entry.insert(tk.END, self.selected_item[1])
            self.token_entry.delete(0, tk.END)
            self.token_entry.insert(tk.END, self.selected_item[2])
            self.frequency.set(self.key_list[self.val_list.index(self.selected_item[3])])
            self.direct.set(self.selected_item[4])
        except IndexError:
            pass

    def start(self):
        url = self.url_entry.get()
        token = self.token_entry.get()
        freq = self.freq[self.frequency.get()]
        direct = self.direct.get()
        auto = self.auto.get()
        if url == '' or token == '':
            messagebox.showerror("Required Fields", " Please fill in all fields.")
            return
        row = db.last()
        if not row:
            self.add_item()
            row = db.last()
            direct = row[4]
        db.update(row[0], url, token, freq, direct, auto)
        self.thread = GetAPI(url=url, token=token, freq=freq, direct=direct)
        self.thread.start()
        print("Started", self.thread)

    def stop(self):
        if self.thread:
            self.thread.stop()
        self.destroy()

    def get_platform(self):
        if sys.platform == 'linux':
            USER_NAME = getpass.getuser()
            file_path = os.path.dirname(os.path.realpath(__file__))
            bat_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % USER_NAME
            with open(bat_path + '\\' + "open.bat", "w+") as bat_file:
                bat_file.write(r'start "" %s' % file_path)


if __name__ == '__main__':
    example = Example()
    example.geometry("620x400")
    example.set_theme("breeze")
    example.title('Iotwhynot API Software ver.1.0.0')
    example.iconphoto(True, PhotoImage(file="image/a.png"))
    example.protocol("WM_DELETE_WINDOW", example.iconify)
    example.mainloop()
