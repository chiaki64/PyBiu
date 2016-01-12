#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @author:Hieda no Chiaki <i@wind.moe>

import hashlib
import logging;logging.basicConfig(level=logging.INFO)
import os
import sys


def str_md5(string):
    obj = hashlib.md5()
    obj.update(string)
    str_hash = obj.hexdigest()
    return str_hash


def file_md5(file_path):
    # 灰常重要的切片
    file_path = file_path[1:-1]
    with open(file_path, 'rb') as f:
        obj = hashlib.md5()
        obj.update(f.read())
        file_hash = obj.hexdigest()
        return file_hash


if __name__ == "__main__":
    if len(sys.argv) == 2:
        file = sys.argv[1]
        if not os.path.exists(file):
            file = os.path.join(os.path.dirname(__file__), file)
            if not os.path.exists(file):
                logging.info("cannot found file")
            else:
                file_md5(file)
        else:
            file_md5(file)
    else:
        logging.info("no filename")
