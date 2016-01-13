#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @author:Hieda no Chiaki <i@wind.moe>

import getopt
import os
import sys
import logging
from src.init import init, usage
from src.md5 import md5
from src.post import post_biu, confirm
from src.dir import que

try:
    import configparser
    import queue
except ImportError:
    import ConfigParser
    from Queue import Queue

logging.basicConfig(level=logging.INFO)


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
        opts, args = getopt.getopt(sys.argv[1:], "hvf:d:", ["update"])
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
                    flag, token, title = post_biu(file)
                    sys.exit() if not flag else confirm(title, file, md5(file, "file"), token)
                    pass
            else:
                if file[0] != "\"":
                    file = "\"" + file + "\""
                flag, token, title = post_biu(file)
                if not flag:
                    sys.exit()
                else:
                    confirm(title, file, md5(file, "file"), token)
                pass

        elif argv in "-d": #上传文件夹
            path = value
            if os.path.isdir(path):
                cnt = 0
                q = que(path)
                try:
                    task_queue = Queue()
                except:
                    task_queue = queue.Queue()
                if not q.empty():
                    logging.info("可以直接上传的歌曲列表")

                    while not q.empty():
                        info = q.get()
                        logging.info(info[1])
                        task_queue.put(info)
                else:
                    print "上传队列为空，请检查目录的合法文件"
                    sys.exit()
                while not task_queue.empty():
                    task = task_queue.get()
                    confirm(task[1], task[2], md5(task[2], "file"), task[0], auto=1)
                pass

            else:
                logging.info("您输入了非法的文件夹路径，请尝试重新输入")
                pass



            pass

        elif argv in "-v":
            try:
                config = configparser.ConfigParser()
                config.read_file(open('./.env'))
            except:
                config = ConfigParser.ConfigParser()
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


