import json
import multiprocessing

import requests

from video import GetVideo


class GetUpMultiVideo(multiprocessing.Process):
    def __init__(self, up_id):
        super().__init__()
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36",
        }
        self.url = "https://api.bilibili.com/x/space/arc/search?mid={}&ps=30&pn=".format(up_id)

    def get_video_bv(self):
        bvs = []
        page = 1

        while True:
            response = requests.get(self.url + str(page), headers=self.headers)
            ret = json.loads(response.text)
            try:
                v_list = ret["data"]["list"]["vlist"]
                for item in v_list:
                    bvs.append(item["bvid"])

                for index, bv in enumerate(bvs):
                    print("当前下载：", index+1)
                    p = GetVideo(bv)
                    p.start()
                    p.join()
            except:
                break
            page += 1

    def run(self):
        self.get_video_bv()


if __name__ == '__main__':

    test = GetUpMultiVideo("517327498")
    test.start()