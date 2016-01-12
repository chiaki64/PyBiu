#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @author:Hieda no Chiaki <i@wind.moe>

import logging;logging.basicConfig(level=logging.INFO)
import requests
import json
import time
import sys

# import urllib.request



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
    #   logging.info(r.text)
    flag, token, up = judge(r.text)
    if flag:
        logging.info("token ->"+token)
        return True, token, title
    elif not up:
        logging.info("是否强制撞车 Y/N")
        try:
            force = raw_input()
        except:
            force = input()
        if force in ["Y", "y"]:
            force = 1
            force_upload, token = post_force(uid, filemd5, title, singer, album, sign, api, force)
            return True, token, title
        return False, "" , title
    else:
        return False, "" , title # 失败


def post_force(uid, filemd5, title, singer, album, sign, api, force):
    upload = {'uid': uid, 'filemd5': filemd5, 'title': title, 'singer': singer, 'album': album, 'sign': sign, 'force': force}
    r = requests.post(api, data=upload)
    try:
        flag, token, upload = judge(unicode(r.text))
        if flag:
            logging.info("token ->"+token)
            return True, token
        else:
            return False, ""  # 失败
    except ValueError:
        return False, ""  # 失败


def judge(text):
    str = json.loads(text)
    if str['success']:
        # logging.info("true")
        token = str['token']
        return True, token, True
    else:
        # logging.info('false')
        if error(str['error_code']) == 2:  # if 'error_code' in str:
            result = str['result']
            # logging.info(result)
            solve(result)
            return False, "", False
        return False, "", True
    pass


def error(error_code):
    if error_code == 1:
        logging.info("sign 签名校检失败")
        return 1
    elif error_code == 2:
        logging.info("系统检测疑似撞车")
        return 2
    elif error_code == 3:
        logging.info("未通过审核的歌曲超过 100 首，请先进入网站『我上传的音乐』删除一部分未通过的文件")
        return 3
    elif error_code == 4:
        logging.info("参数不齐，至少歌曲名不能为空")
        return 4
    elif error_code == 5:
        logging.info("服务器已存在该文件（撞 MD5）")
        return 5
    else:
        logging.info("unknown result.")
        return 6


def solve(string):
    # string = [{'level': '1', 'album': 'Rwby (Songs)', 'title': 'This Will Be The Day (Featuring Casey Lee Williams)',
    #            'sid': '6574', 'singer': 'Jeff Williams', 'score': 5.5},
    #           {'level': '1', 'album': 'Rwby (Songs)', 'title': 'This Will Be The Day (Featuring Casey Lee Williams)',
    #            'sid': '6574', 'singer': 'Jeff Williams', 'score': 5.5}]
    # s = json.dumps(string)
    # logging.info(string)
    logging.info("疑似撞车的歌曲:")
    for res in string:
        logging.info("Title: " + res['title'] + " | album: " + res['album'] + " | singer: " + res['singer'] + " | sid: " +
              res['sid'] + " | score : %.1f" % res['score'])
    pass


def post_biu(file):
    _title, _artist, _album, _flag = getID3(file)
    try:
        if _flag == 0:
            logging.info("码率不合 请重现检察")
            raise Exception  # 自定义错误
        if _flag == 2:
            logging.info("Title不完整 拒绝上传")
            raise Exception  # 自定义错误
    except Exception:
        return 0, "", ""
    logging.info("Title -> " + _title)
    logging.info("Artist -> " + _artist)
    logging.info("Album -> " + _album)
    _md5 = file_md5(file)
    _uid, _key, _api = uid()
    _sign_str = sign(_uid, _md5, _key, _title, _artist, _album)
    # logging.info(_sign_str)
    flag, token, title = post(_uid, _md5, _title, _artist, _album, _sign_str, _api)
    if flag:
        logging.info("允许上传")
        return 1, token, title
    logging.info("取消上传.")
    return 0, "", title


def post_file(path, key, token):
    path = path[1:-1]
    file = {'file': open(path, 'rb')}
    upload = { 'key': key, 'x:md5': key, 'token': token}
    r = requests.post("http://upload.qiniu.com/", files=file,data=upload)
    status = r.status_code
    if status == 200:
        return True
    return False


def confirm(title, path, key, token):
    logging.info("是否上传？Y/N")
    try:
        choose = raw_input()
    except:
        choose = input()
    if choose in ["Y", "y"]:
        # progress_test()
        if post_file(path, key, token):
            logging.info("成功上传  " + title.encode('gbk'))
        else:
            logging.info("未知原因失败")
    else:
        logging.info("取消上传.")
        pass

    pass



#  异步
# def progress_test():
#     bar_length=20
#     for percent in range(0, 100):
#         hashes = '#' * int(percent/100.0 * bar_length)
#         spaces = ' ' * (bar_length - len(hashes))
#         sys.stdout.write("\rPercent: [%s] %d%%"%(hashes + spaces, percent))
#         sys.stdout.flush()
#         time.sleep(1)




if __name__ == "__main__":
    pass

