#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @author:Hieda no Chiaki <i@wind.moe>

import logging
import os
import threading
from src.post import post_biu

try:
    from Queue import Queue
except:
    import queue

logging.basicConfig(level=logging.INFO)


def que(_path):
    try:
        q = Queue()
    except:
        q = queue.Queue()

    path = r"D:\Python\WorkSpace\PyBiu\test"
    for filename in os.listdir(_path):
        # print filename.decode('gbk')
        suffix = os.path.splitext(filename)[1]  # .decode('gbk')
        # print suffix
        if suffix[1:] in ["mp3", "aac", "flac", "ape", "wav", "tta", "tak", "alac"]:
            logging.info(filename.decode('gbk'))  #.decode('gbk')
            logging.info(_path + os.sep + filename)  # .decode('gbk')
            string = "\""+_path + os.sep + filename+"\""
            flag, token, title = post_biu(string)  #日文曲出错 .decode('gbk')
            if flag:
                q.put([token, title, string.decode('gbk')])
                # info = q.get()
                # # print "Queue is ----------->" + info[1]
                logging.info(filename.decode('gbk'))

    return q
