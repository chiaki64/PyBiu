#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @author:Hieda no Chiaki <i@wind.moe>

import logging;logging.basicConfig(level=logging.INFO)
from src.md5 import str_md5, file_md5
from src.id3 import getID3
try:
    import configparser
except ImportError:
    import ConfigParser

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
        config.readfp(open('./.env'))
    finally:
        uid = config.get("Config", "UID")
        key = config.get("Config", "KEY")
        api = config.get("Config", "API")
        return uid, key, api


def sign(uid, md5, key, title, artist, album):
    str = uid + md5 + title + artist + album + key
    sign_str = str_md5(str.encode('utf-8'))
    return sign_str


if __name__ == "__main__":
    pass
