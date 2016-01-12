aac码率大于200，MP3码率大于300

可能获取不到id3

--remark

强制撞

文件类型

文件路径强制加""


上传历史

@property

重试3次 失败就抛一场
 for i in range(0, 3):
            try:
                response = requests.get(url, headers=headers)
                # 防止403等
                if response.status_code != 200:
                    raise ValueError()
                return response.content
            except Exception as e:
                if i == 2:
                    raise e
                continue

string = input()
logging.info(string)
获取输入

apt-get install ffmpeg 
osx brew install ffmpeg