import threading
import requests
import time
import datetime
import os
import errno
import signal


class GetAPI(threading.Thread):
    def __init__(self, url, token, freq, direct,  *args, **kwargs):
        super(GetAPI, self).__init__(*args, **kwargs)
        self.url = url
        self.token = token
        self.freq = freq
        self.direct = direct
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
        for i in range(100):
            response = requests.get(self.url, headers={"Authorization": f"{self.token}"})
            print(f"{i} Working: {response}")
            f = open(os.path.join(f'{self.direct}/data.json'), 'wb')
            f.write(response.content)
            f.close()
            time.sleep(1)
