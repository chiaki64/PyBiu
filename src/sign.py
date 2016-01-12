#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @author:Hieda no Chiaki <i@wind.moe>

import logging;logging.basicConfig(level=logging.INFO)
try:
    import configparser
except ImportError:
    import ConfigParser
from src.md5 import str_md5, file_md5
from src.id3 import getID3


def uid():
    try:
        config = configparser.ConfigParser()
    except:
        config = ConfigParser.ConfigParser()
    try:
        # try:
        config.read_file(open('./.env'))
        # except:
        #     config.read_file(open('../.env'))
    except:
        # try:
        config.readfp(open('./.env'))
        # sections = config.sections()
        # logging.info(sections)
        # except:
        #     config.readfp(open('../.env'))
        #     sections = config.sections()
        #     logging.info(sections)
    finally:
        uid = config.get("Config", "UID")
        key = config.get("Config", "KEY")
        api = config.get("Config", "API")
        # logging.info("log: uid = " + uid)
        # logging.info("log: key = " + key)
        return uid, key, api


def sign(uid, md5, key, title, artist, album):
    str = uid + md5 + title + artist + album + key
    sign_str = str_md5(str.encode('utf-8'))
    return sign_str


if __name__ == "__main__":
    uid, key = uid()
    title, artist, album = getID3('1')
    md5 = file_md5("D:\\Python\\WorkSpace\\Biu.moe_Uploader\\test\\This.mp3")
    logging.info(md5)
    tmp = sign(uid, md5, key, title, artist, album)
    logging.info("==Sign== "+tmp)
    pass
