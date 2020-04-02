import getpass
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from db import Database
from tkinter import messagebox, filedialog
from ttkwidgets.autocomplete import AutocompleteCombobox
from get_api import GetAPI
from tkinter import *
from win32com.client import Dispatch
import sys, os
import winreg as reg

db = Database('store.db')


class Example(ThemedTk):
    def __init__(self):
        ThemedTk.__init__(self, themebg=True)
        self.url_label = ttk.Label(self, text="Enter request URL")
        self.url_entry =  AutocompleteCombobox(self, completevalues=["https://iotwhynot.com/chip_manager/read_data_api"])

        self.token_label = ttk.Label(self, text="Authorization")
        self.token_entry = ttk.Entry(self, width=70, textvariable=tk.StringVar())
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
        self.frq_option = ttk.OptionMenu(self, self.frequency, *self.freq.keys())

        self.auto = tk.BooleanVar(value=True)
        self.checked = ttk.Checkbutton(self, text="Automatically start the software with windows", variable=self.auto)

        self.direct = tk.StringVar()
        self.sto_label = tk.Label(self, textvariable=self.direct)
        self.sto_button = ttk.Button(self, text="Please select the path to direct the returned data", command=self.file_dialog)

        # self.save_button = ttk.Button(self, text="Save", command=self.add_item)
        self.start_button = ttk.Button(self, text="Start", command=self.start)
        self.stop_button = ttk.Button(self, text="Stop", command=self.stop)

        self.status_label = ttk.Label(self, text="Status:")
        self.status = tk.Label(self, text="Inactive (dead)", fg="red", font=("Courier", 11))
        self.status_label.grid(row=6, column=0)
        self.status.grid(row=6, column=1, sticky='w')
        # self.abc = tk.BooleanVar(value=True)
        # self.status = ttk.Checkbutton(self, text="", variable=self.abc)
        # self.radio = ttk.Radiobutton(self, text="Radio two", value=True)
        # self.status.config(text="ksnvlk", variable=tk.BooleanVar(value=False))
        # self.radio.config(text="Radio sbvk", value=False)

        self.license = ttk.Label(self, text="© Copyright Teslateq Co., Ltd.")
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

        self.start_button.grid(row=6, column=1, pady=15, sticky='sn')
        self.stop_button.grid(row=6, column=1, pady=15, sticky='e')
        # self.save_button.grid(row=6, column=1, sticky='e')
        # self.status.grid(row=6, column=0, pady=15, sticky='w')
        # self.radio.grid(row=7, column=1, **sticky)
        self.license.grid(row=8, column=0, columnspan=3, sticky='s')

    def file_dialog(self):
        filename = filedialog.askdirectory()
        self.direct.set(filename)

    def get_list(self):
        row = db.last()
        print('get_list_row', row)
        if row:
            if row[5] == 1: # Auto startup
                self.thread = GetAPI(url=row[1], token=row[2], freq=row[3], direct=row[4],  tkinter=self)
                self.thread.start()
            self.url_entry.delete(0, tk.END)
            self.url_entry.insert(tk.END, row[1])
            self.token_entry.delete(0, tk.END)
            self.token_entry.insert(tk.END, row[2])
            self.frequency.set(self.key_list[self.val_list.index(row[3])])
            self.direct.set(row[4])
            self.auto.set(row[5])

    def add_item(self):
        direct = self.direct.get()
        if not direct:
            dirName = 'downloads'
            if not os.path.exists(dirName):
                os.mkdir(dirName)
            direct = f'{os.getcwd()}\{dirName}'
        auto = self.auto.get()
        print("auto", auto)
        if auto:
            self.create_shortcut_auto_startup()
        db.insert(self.url_entry.get(), self.token_entry.get(),  self.freq[self.frequency.get()], direct,  auto)
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
            auto = row[5]
            self.status.config(text=f"Changes saved", fg="black")
        if auto == 1:  # auto startup
            self.create_shortcut_auto_startup()
        else:
            self.remove_shortcut()
        my_tuple = (row[0], url, token, freq, direct, auto)
        self.thread = GetAPI(url=url, token=token, freq=freq, direct=direct, tkinter=self)
        self.thread.start()
        if my_tuple != row:
            self.status.config(text=f"Changes saved", fg="black")
            db.update(row[0], url, token, freq, direct, auto)
        print("Started", self.thread)

    def stop(self):
        if self.thread:
            self.thread.stop()
        self.destroy()

    def create_shortcut_auto_startup(self):
        if sys.platform == 'win32':
            USER_NAME = getpass.getuser()
            desktop = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % USER_NAME
            path = os.path.join(desktop, 'iotwhynot.lnk')  # path to where you want to put the .lnk
            target = f'{os.path.dirname(os.path.realpath(__file__))}\main.exe'
            icon = f'{os.path.dirname(os.path.realpath(__file__))}\image\logo.ico'
            file_path = f'{os.path.dirname(os.path.realpath(__file__))}'
            shell = Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(path)
            shortcut.Targetpath = target
            shortcut.WorkingDirectory = file_path
            shortcut.IconLocation = icon
            shortcut.WindowStyle = 7  # 7 - Minimized, 3 - Maximized, 1 - Normal
            shortcut.save()
        """
        intWindowStyle - Description
        1 Activates and displays a window. If the window is minimized or maximized, the system restores it to its original size and position.
        3 Activates the window and displays it as a maximized window.
        7 Minimizes the window and activates the next top-level window.
        """

    def remove_shortcut(self):
        if sys.platform == 'win32':
            USER_NAME = getpass.getuser()
            path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\iotwhynot.lnk' % USER_NAME
            try:
                os.remove(path)
            except FileNotFoundError:
                pass

if __name__ == '__main__':
    example = Example()
    example.geometry("640x370")  # width x height
    example.resizable(width=FALSE, height=FALSE) # fix frames
    example.set_theme("breeze")
    example.title('Iotwhynot API Software ver.1.0.0')
    example.iconphoto(True, PhotoImage(file="image/a.png"))
    example.protocol("WM_DELETE_WINDOW", example.iconify)
    example.mainloop()
