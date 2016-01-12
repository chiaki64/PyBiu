#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @author:Hieda no Chiaki <i@wind.moe>

import getopt
import os
import sys
import logging;logging.basicConfig(level=logging.INFO)
from src.init import init, usage
from src.md5 import file_md5
from src.post import post_biu, confirm
try:
    import configparser
except ImportError:
    import ConfigParser


if len(sys.argv) == 1:
    """检察上传环境"""
    logging.info("Checking System Environments...")
    try:
        import requests
    except:
        logging.info('Please install requests. [pip install requests]')
        exit(1)
    init()
    # 重试三次  如果无法连接则抛出网络异常
    logging.info("Connect to Biu.moe...")
    for i in range(0, 3):
        try:
            r = requests.get('http://biu.moe/', timeout=3)
            if r.status_code != 200:
                raise ValueError()
            break
        except Exception as e:
            if i == 2:
                logging.info("Fail. Please check your internet connection.")
                exit(1)
            continue
    logging.info("Success.")

else:
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hvf:", ["update"])
    except getopt.GetoptError:
        sys.exit()

    for argv, value in opts:
        if argv in "-f":
            file = value
            if not os.path.exists(file):
                file = os.path.split(os.path.realpath(__file__))[0] + file
                logging.info(file)
                if not os.path.exists(file):
                    logging.info("找不到文件.请尝试用双引号将文件绝对路径包括起来.")
                else:
                    logging.info("test")
                    flag, token = post_biu(file)
                    sys.exit() if not flag else logging.info("lol")
                    pass
            else:
                if file[0] != "\"":
                    file = "\"" + file + "\""
                flag, token, title = post_biu(file)
                if not flag:
                    sys.exit()
                else:
                    confirm(title, file, file_md5(file), token)
                pass

        elif argv in "-v":
            try:
                config = configparser.ConfigParser()
            except:
                config = ConfigParser.ConfigParser()
            try:
                config.read_file(open('./.env'))
            except:
                config.readfp(open('./.env'))
            version = config.get("Environment", "VERSION")
            logging.info(version)
        elif argv in "-h":
            usage()
            sys.exit()
        else:
            pass

    for argv in args:
        if argv in "update":
            logging.info("update")
        elif argv in "test":
            logging.info("test.")
        else:
            pass


