#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @author:Hieda no Chiaki <i@wind.moe>

import logging
import os
import platform
import shutil

try:
    import configparser
except ImportError:
    import ConfigParser

logging.basicConfig(level=logging.INFO)


def init():
    try:
        config = configparser.ConfigParser()
    except:
        config = ConfigParser.ConfigParser()
    try:
        config.read_file(open('./.env'))
    except:
        config.readfp(open('./.env'))
    logging.info("Set UID")
    try:
        config.set("Config", "uid", raw_input())
    except:
        config.set("Config", "uid", input())
    logging.info("Set KEY")
    try:
        config.set("Config", "key", raw_input())
    except:
        config.set("Config", "key", input())
    logging.info("Set Python Version")
    config.set("Config", "python", platform.python_version())
    logging.info("Set System Version")
    config.set("Config", "system", system())
    logging.info("Set Post API")
    config.set("Config", "api", "https://api.biu.moe/Api/createSong")
    config.write(open('./.env', "r+"))


def system():
    """"""
    s = platform.system()
    if s == 'Windows':
        sys = 'Windows'
        return sys
    elif s == 'Darwin':
        sys = 'MacOS'
        return sys
    else:
        sys = 'Linux'
        return sys


def exist():
    if os.path.exists('../.env'):
        if os.path.exists('../.env.example'):
            shutil.copy('../.env.example', '../.env.bak')
            os.renames('../.env.bak', '../.env')
        pass
    pass


def usage():
    logging.info("help")
    pass


if __name__ == "__main__":
    pass
