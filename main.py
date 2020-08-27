from multi_video import GetUpMultiVideo
from video import GetVideo


def main():
    # BV1Pt4y1Q7Yn
    print("-----欢迎使用本软件！-----")
    print("1.输入bv号下载单视频")
    print("2.下载指定up全部视频")
    print("------------------------")
    option = input("请输入序号执行操作：")
    if option == "1":
        bv = input("请输入视频bv号：")
        GetVideo(bv).start()
    elif option == "2":
        up_id = input("请输入up个人空间url中的id：")
        GetUpMultiVideo(up_id).start()


if __name__ == '__main__':
    main()
