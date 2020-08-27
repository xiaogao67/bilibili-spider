import multiprocessing
import os
import re

import requests


class FileDownload(multiprocessing.Process):
    """下载音频文件"""

    def __init__(self, base_url, headers, title, url, typ):
        super().__init__()
        # 参数
        self.base_url = base_url
        self.headers = headers
        self.title = title
        self.url = url
        self.typ = typ
        # 指定每次下载数据大小/m
        self.begin = 0
        self.end = 1024 * 1024
        self.flag = 0

    def run(self):
        self.headers.update({'Referer': self.base_url})
        if self.typ == 0:
            filename = self.title + ".flv"
        else:
            filename = self.title + ".mp3"
        res = requests.Session()
        while True:
            # 添加请求头键值对,写上 range:请求字节范围
            self.headers.update({'Range': 'bytes=' + str(self.begin) + '-' + str(self.end)})
            # 获取视频分片
            res = requests.get(url=self.url, headers=self.headers, verify=False)

            range_len = res.headers.get("Content-Range")
            try:
                max_size = re.search("bytes (\d*)-(\d*)/(\d*)", range_len).group(3)
            except:
                pass

            progress = int(self.begin * 100.0 / int(max_size))
            if progress <= 100:
                print(str(progress) + "%" + "  " + filename)
            else:
                print(str(100) + "%" + "  " + filename)

            if res.status_code != 416:
                # 响应码不为416时有数据，由于我们不是b站服务器，最终那个数据包的请求range肯定会超出限度，所以传回来的http状态码是416而不是206
                self.begin = self.end + 1
                self.end = self.end + 1024 * 1024 - 1
            else:
                self.headers.update({'Range': str(self.end + 1) + '-'})
                res = requests.get(url=self.url, headers=self.headers, verify=False)
                self.flag = 1
            with open("./video-files/" + filename, 'ab') as fp:
                fp.write(res.content)
                fp.flush()
            if self.flag == 1:
                fp.close()
                print("下载完毕", filename)
                break


class VideoJoinAudio(multiprocessing.Process):
    """合并flv跟mp3文件"""

    def __init__(self, title):
        super().__init__()
        self.title = title
        self.flv_file = title + ".flv"
        self.mp3_file = title + ".mp3"
        self.path = os.getcwd() + "\\video-files\\"

    def run(self):
        cmd = "ffmpeg -i " + self.path + self.mp3_file + " -i " + self.path + self.flv_file + " " + self.path + self.title + ".mp4"
        print("合并音频文件中...", self.title)
        os.system(cmd)

        if os.path.exists(self.path + self.flv_file):
            os.remove(self.path + self.flv_file)
        if os.path.exists(self.path + self.mp3_file):
            os.remove(self.path + self.mp3_file)

        print("合并完成：", self.title + ".mp4")
