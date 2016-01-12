#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @author:Hieda no Chiaki <i@wind.moe>

import hashlib
import logging
import os
import sys

logging.basicConfig(level=logging.INFO)


def md5(string, type):
    if type == "str":
        obj = hashlib.md5()
        obj.update(string)
        str_hash = obj.hexdigest()
        return str_hash
    elif type == "file":
        # 灰常重要的切片 切掉前后两个引号
        string = string[1:-1]
        with open(string, 'rb') as f:
            obj = hashlib.md5()
            obj.update(f.read())
            string_hash = obj.hexdigest()
            return string_hash
    return None


# def str_md5(string):
#     obj = hashlib.md5()
#     obj.update(string)
#     str_hash = obj.hexdigest()
#     return str_hash
#
#
# def file_md5(file_path):
#     # 灰常重要的切片 切掉前后两个引号
#     file_path = file_path[1:-1]
#     with open(file_path, 'rb') as f:
#         obj = hashlib.md5()
#         obj.update(f.read())
#         file_hash = obj.hexdigest()
#         return file_hash


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
