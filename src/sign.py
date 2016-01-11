#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @author:Hieda no Chiaki <i@wind.moe>

import configparser
from src.md5 import str_md5, file_md5
from src.id3 import getID3


def uid():
    config = configparser.ConfigParser()
    try:
        config.read_file(open('./.env'))
    except:
        config.read_file(open('../.env'))
    finally:
        uid = config.get("Config", "UID")
        key = config.get("Config", "KEY")
        api = config.get("Config", "API")
        # print("log: uid = " + uid)
        # print("log: key = " + key)
        return uid, key, api


def sign(uid, md5, key, title, artist, album):
    str = uid + md5 + title + artist + album + key
    sign_str = str_md5(str.encode('utf-8'))
    return sign_str


if __name__ == "__main__":
    uid, key = uid()
    title, artist, album = getID3('1')
    md5 = file_md5("D:\\Python\\WorkSpace\\Biu.moe_Uploader\\test\\This.mp3")
    print(md5)
    tmp = sign(uid, md5, key, title, artist, album)
    print("==Sign== "+tmp)
    pass
