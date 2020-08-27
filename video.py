import json
import multiprocessing
import re

from lxml import etree
import requests

from download import FileDownload, VideoJoinAudio


class GetVideo(multiprocessing.Process):
    def __init__(self, bv):
        super().__init__()
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36",
        }
        self.base_url = "https://www.bilibili.com/video/" + bv

    def request_data(self):
        response = requests.get(self.base_url, headers=self.headers)
        # 获取视频标题
        html = etree.HTML(response.text)
        try:
            title = html.xpath("//h1[@class='video-title']/span/text()")[0]
        except Exception as e:
            print(e)
            return

        # 获取视频文件url
        result = re.findall(r"\<script\>window\.__playinfo__=(.*?)\</script\>", response.text)
        ret_dict = json.loads(result[0])

        return ret_dict, title

    def run(self):
        ret_dict, title = self.request_data()
        # 获取视频url
        video_url = ret_dict["data"]["dash"]["video"][0]["baseUrl"]
        audio_url = ret_dict["data"]["dash"]["audio"][0]["baseUrl"]

        video = FileDownload(self.base_url, self.headers, title, video_url, 0)
        audio = FileDownload(self.base_url, self.headers, title, audio_url, 1)
        video.start()
        audio.start()
        video.join()
        audio.join()
        # 合并音频
        VideoJoinAudio(title).start()
