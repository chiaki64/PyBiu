#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @author:Hieda no Chiaki <i@wind.moe>

import logging
from src.md5 import md5

try:
    import configparser
except ImportError:
    import ConfigParser

logging.basicConfig(level=logging.INFO)


def uid():
    try:
        config = configparser.ConfigParser()
    except:
        config = ConfigParser.ConfigParser()
    try:
        config.read_file(open('./.env'))
    except:
        config.readfp(open('./.env'))
    finally:
        uid = config.get("Config", "UID")
        key = config.get("Config", "KEY")
        api = config.get("Config", "API")
        return uid, key, api


def sign(_uid, _md5, _key, _title, _artist, _album):
    str = _uid + _md5 + _title + _artist + _album + _key
    sign_string = md5(str.encode('utf-8'), "str")
    return sign_string


if __name__ == "__main__":
    pass
