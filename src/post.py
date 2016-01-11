#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @author:Hieda no Chiaki <i@wind.moe>

import requests
import json

from src.init import usage
from src.id3 import getID3
from src.md5 import str_md5, file_md5
from src.sign import sign, uid


def post(uid, filemd5, title, singer, album, sign, api):
    # payload = {'uid': '830', 'filemd5': '81842c14f56bb3d2bf49f42cb32005a8', 'title': 'This Will Be the Day',
    #            'singer': 'Jeff Williams;Casey Lee Williams', 'album': 'RWBY Volume 1 Soundtrack',
    #            'sign': '9cc0c9913190b0973b18aee175b22efa'}
    upload = {'uid': uid, 'filemd5': filemd5, 'title': title, 'singer': singer, 'album': album, 'sign': sign}
    r = requests.post(api, data=upload)
    #   print(r.text)
    flag, token = judge(r.text)
    if flag:
        print("token ->"+token)
        return True, token
    else:
        return False, ""  # 失败


def judge(text):
    str = json.loads(text)
    if str['success']:
        # print("true")
        token = str['token']
        return True, token
    else:
        # print('false')
        if error(str['error_code']) == 2:  # if 'error_code' in str:
            result = str['result']
            # print(result)
            solve(result)
        return False, ""
    pass


def error(error_code):
    if error_code == 1:
        print("sign 签名校检失败")
        return 1
    elif error_code == 2:
        print("系统检测疑似撞车")
        return 2
    elif error_code == 3:
        print("未通过审核的歌曲超过 100 首，请先进入网站『我上传的音乐』删除一部分未通过的文件")
        return 3
    elif error_code == 4:
        print("参数不齐，至少歌曲名不能为空")
        return 4
    elif error_code == 5:
        print("服务器已存在该文件（撞 MD5）")
        return 5
    else:
        print("unknown result.")
        return 6


def solve(string):
    # string = [{'level': '1', 'album': 'Rwby (Songs)', 'title': 'This Will Be The Day (Featuring Casey Lee Williams)',
    #            'sid': '6574', 'singer': 'Jeff Williams', 'score': 5.5},
    #           {'level': '1', 'album': 'Rwby (Songs)', 'title': 'This Will Be The Day (Featuring Casey Lee Williams)',
    #            'sid': '6574', 'singer': 'Jeff Williams', 'score': 5.5}]
    # s = json.dumps(string)
    # print(string)
    print("疑似撞车的歌曲:")
    for res in string:
        print("Title: " + res['title'] + " | album: " + res['album'] + " | singer: " + res['singer'] + " | sid: " +
              res['sid'] + " | score : %.1f" % res['score'])
    pass


def post_biu(file):
    _title, _artist, _album, _flag = getID3(file)
    try:
        if _flag == 0:
            print("码率不合 请重现检察")
            raise Exception  # 自定义错误
        if _flag == 2:
            print("Title不完整 拒绝上传")
            raise Exception  # 自定义错误
    except Exception:
        return 0, ""
    print("Title -> " + _title)
    print("Artist -> " + _artist)
    print("Album -> " + _album)
    _md5 = file_md5(file)
    _uid, _key, _api = uid()
    _sign_str = sign(_uid, _md5, _key, _title, _artist, _album)
    # print(_sign_str)
    flag, token = post(_uid, _md5, _title, _artist, _album, _sign_str, _api)
    if flag:
        print("允许上传")
    return 1, token


def post_file(path, key, token):
    path = path[1:-1]
    file = {'file': open(path, 'rb')}
    upload = { 'key': key, 'x:md5': key, 'token': token}
    r = requests.post("http://upload.qiniu.com/", files=file,data=upload)
    status = r.status_code
    if status == 200:
        return True
    return False


def confirm(path, key, token):
    print("是否上传？Y/N")
    choose = input()
    if choose == "Y":
        if post_file(path, key, token):
            print("上传成功.")
        else:
            print("位置原因失败")
    else:
        pass

    pass

if __name__ == "__main__":
    pass

