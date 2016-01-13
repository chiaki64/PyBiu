#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @author:Hieda no Chiaki <i@wind.moe>

import json
import requests
import logging
import sys
import os
import time
import random
from src.id3 import getID3
from src.md5 import md5
from src.sign import sign, uid
# from src.dir import que
import pycurl


logging.basicConfig(level=logging.INFO)


def post(uid, filemd5, title, singer, album, sign, api):
    upload = {'uid': uid, 'filemd5': filemd5, 'title': title, 'singer': singer, 'album': album, 'sign': sign}
    r = requests.post(api, data=upload, verify=False)  # dirty hack
    flag, token, up = judge(r.text)
    if flag:
        logging.info("token ->" + token)
        return True, token, title
    elif not up:
        logging.info("是否强制撞车 Y/N")
        try:
            force = raw_input()
        except NameError:
            force = input()
        if force in ["Y", "y"]:
            force = 1
            force_upload, token = post_force(uid, filemd5, title, singer, album, sign, api, force)
            return True, token, title
        return False, "", title
    else:
        return False, "", title  # 失败


def post_force(uid, filemd5, title, singer, album, sign, api, force):
    upload = {'uid': uid, 'filemd5': filemd5, 'title': title, 'singer': singer, 'album': album, 'sign': sign,
              'force': force}
    r = requests.post(api, data=upload, verify=False)
    try:
        flag, token, upload = judge(r.text)
        if flag:
            logging.info("token ->" + token)
            return True, token
        else:
            return False, ""  # 失败
    except ValueError:
        return False, ""  # 失败


def judge(text):
    str = json.loads(text)
    logging.info(str)
    if str['success']:
        token = str['token']
        return True, token, True
    else:
        if error(str['error_code']) == 2:  # if 'error_code' in str:
            result = str['result']
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
        logging.info("未通过审核的歌曲超过 100 首 请先进入网站『我上传的音乐』删除一部分未通过的文件")
        return 3
    elif error_code == 4:
        logging.info("参数不齐 至少歌曲名不能为空")
        return 4
    elif error_code == 5:
        logging.info("服务器已存在该文件（撞 MD5）")
        return 5
    elif error_code == 6:
        logging.info("服务器录入失败 如果发现请通知管理员")
        return 6
    elif error_code == 7:
        logging.info("服务器菌正在休息，请不要打扰它~")
        return 7
    else:
        logging.info("未知原因")
        return 100


def solve(string):
    logging.info("疑似撞车的歌曲:")
    for res in string:
        logging.info(
                "Title: " + res['title'] + " | album: " + res['album'] + " | singer: " + res['singer'] + " | sid: " +
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
    _md5 = md5(file, "file")  # file_md5
    _uid, _key, _api = uid()
    _sign_str = sign(_uid, _md5, _key, _title, _artist, _album)
    flag, token, title = post(_uid, _md5, _title, _artist, _album, _sign_str, _api)
    if flag:
        logging.info("允许上传")
        return 1, token, title
    logging.info("上传已取消")
    return 0, "", title


def post_file(path, key, token):
    path = path[1:-1]
    file = {'file': open(path, 'rb')}
    upload = {'key': key, 'x:md5': key, 'token': token}
    r = requests.post("http://upload.qiniu.com/", files=file, data=upload)
    status = r.status_code
    if status == 200:
        return True
    return False


def confirm(title, path, key, token, auto=0):
    if auto == 0:
        logging.info("是否上传？Y/N")
        try:
            choose = raw_input()
        except NameError:
            choose = input()
        if choose in ["Y", "y"]:
            if post_file_curl(path, key, token):
                logging.info("成功上传  " + title)
            else:
                logging.info("未知原因失败")
        else:
            logging.info("取消上传.")
            pass
        pass
    elif auto == 1:
        if post_file(path, key, token):
            logging.info("成功上传  " + title.encode('gbk'))
        else:
            logging.info("未知原因失败")


def progress(_, __, upload_t, upload_d):
    if upload_t > 0.0 and upload_t >= upload_d:
        # print("Total to upload", upload_t)
        # print("Total uploaded", upload_d)
        bar_length = 20
        percent = float(upload_d) / float(upload_t) * 100
        # print(percent)
        hashes = '#' * int(percent/100.0 * bar_length)
        spaces = ' ' * (bar_length - len(hashes))
        sys.stdout.write("\rPercent: [%s] %d%%" % (hashes + spaces, percent))
        sys.stdout.flush()
    elif upload_t != 0.0 and upload_t <= upload_d:
        sys.stdout.flush()
        sys.stdout.write("\rPercent: [####################] 100%\n")
        sys.stdout.flush()


def my_urlencode(string):
    reprStr = repr(string).replace(r'\x', '%')
    return reprStr[1:-1]


def post_file_curl(path, key, token):
    c = pycurl.Curl()
    c.setopt(c.POST, 1)
    # if path[0] == "\"":
    path = path[1:-1]

    if os.path.exists(path):
        suffix = os.path.splitext(path)[1]
        # A fucking dirty hack - rename file
        while True:
            number = random.randint(10, 100000)
            if not os.path.exists(os.path.split(path)[0] + "/" + str(number) + suffix):
                newpath = os.path.split(path)[0] + "/" + str(number) + suffix
                break
        os.rename(path, newpath)
        print("rename" + newpath)

    bak_path = newpath
    print(path)
    fields = [('file', (c.FORM_FILE, newpath.encode('gbk'))),
              ('token', token),
              ('key', key),
              ('x:md5', key)]
    c.setopt(c.VERBOSE, 1)
    c.setopt(c.URL, "http://upload.qiniu.com/")
    c.setopt(c.HTTPPOST,  fields)
    c.setopt(c.NOPROGRESS, 0)
    c.setopt(c.PROGRESSFUNCTION, progress)
    c.setopt(pycurl.CONNECTTIMEOUT, 60)
    c.setopt(pycurl.TIMEOUT, 600)
    try:
        info = c.perform()
        print(info)
        print(fields)
        if c.getinfo(c.HTTP_CODE) == 200:
            os.rename(newpath, path)
            print("rename" + path)
            return True
    except pycurl.error as e:
        print(e)
        sys.stdout.write("File no Found!")
        return False
    if os.path.exists(newpath):
        os.rename(newpath, path)
        print("rename" + path)

    c.close()
    return False



if __name__ == "__main__":

    pass
