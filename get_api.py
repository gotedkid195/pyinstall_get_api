import threading
import requests
import time
import datetime
import os
import errno


class GetAPI(threading.Thread):
    def __init__(self, url, token, *args, **kwargs):
        super(GetAPI, self).__init__(*args, **kwargs)
        self.url = url
        self.token = token
        self.stop_request = threading.Event()

    def stop(self):
        self.stop_request.set()

    def run(self) -> None:
        while True:
            response = requests.get(self.url, headers={"Authorization": f"{self.token}"})
            print(f"Get api {response}")
            # filename = '/abc/'
            # os.makedirs(filename)
            # dir_path = os.path.dirname(os.path.realpath(__file__))
            # print(dir_path)
            # os.chdir(dir_path)
            # os.makedirs('abc/', exist_ok=True)
            # access_rights = 0o755
            # os.mkdir('abc', access_rights)

            #
            # folder = 'abc1'
            # if not os.path.exists(folder):
            #     os.mkdir(folder)
            # elif not os.path.isdir(folder):
            #     return
            # f = open(os.path.join('abc1/data.json'), 'wb')


            f = open(os.path.join('/home/canhnguyen/part_manager/data.json'), 'wb')
            f.write(response.content)
            f.close()


            # with open('/abc/data.json', 'wb') as f:
            #     f.write(response.content)
            time.sleep(1)
