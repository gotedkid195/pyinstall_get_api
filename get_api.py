import threading
import requests
import time
import datetime
import os
import errno
import signal


class GetAPI(threading.Thread):
    def __init__(self, url, token, freq, direct, tkinter, *args, **kwargs):
        super(GetAPI, self).__init__(*args, **kwargs)
        self.url = url
        self.token = token
        self.freq = freq
        self.direct = direct
        self.tkinter = tkinter
        self._stop_event = threading.Event()

    def stop(self):
        # print("current_thread",threading.current_thread())
        # print("activeCount",threading.activeCount())
        # print("enumerate",threading.enumerate())

        self._stop_event.set()
        self.join(1)

        os.kill(os.getpid(), signal.SIGTERM)
        # print("stop thread", self)
        # print("current_thread",threading.current_thread())
        # print("activeCount",threading.activeCount())
        # print("enumerate",threading.enumerate())

    def run(self) -> None:
        while True:
            response = requests.get(f"{self.url}", headers={"Authorization": f"{self.token}"})
            print(f"Working: {response}")
            # open(os.path.join(f'{self.direct}\data.json'), 'wb').write(response.content)
            f = open(os.path.join(f'{self.direct}/data.json'), 'wb')
            f.write(response.content)
            f.close()
            status_code = response.status_code
            if status_code == 200:
                self.tkinter.status.config(text="Active (running) ", fg="green")
            elif status_code == 500:
                self.tkinter.status.config(text=f"Error [{status_code}]", fg="red")
                print(response)
            elif status_code == 401:
                self.tkinter.status.config(text=f"Wrong token", fg="red")
            elif status_code == 404:
                self.tkinter.status.config(text=f"Wrong url", fg="red")
            else:
                self.tkinter.status.config(text=f"Wrong [{status_code}]", fg="red")
                print(response)
            time.sleep(self.freq)
            if status_code == 500:
                self.tkinter.status.config(text=f"Error [{status_code}]", fg="black")
                print(response)
            elif status_code == 401:
                self.tkinter.status.config(text=f"Wrong token", fg="black")
            elif status_code == 404:
                self.tkinter.status.config(text=f"Wrong url", fg="black")
