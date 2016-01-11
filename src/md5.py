#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @author:Hieda no Chiaki <i@wind.moe>

import hashlib
import os
import sys
# import time


def str_md5(str):
    obj = hashlib.md5()
    obj.update(str)
    str_hash = obj.hexdigest()

    # print(str_hash)

    return str_hash


def file_md5(file_path):
    # start = time.time()
    # 灰常重要的切片
    file_path = file_path[1:-1]
    with open(file_path, 'rb') as f:
        obj = hashlib.md5()
        obj.update(f.read())
        file_hash = obj.hexdigest()

        # print(file_hash)

        # end = time.time()
        # interval = (end - start)
        # print(interval)
        return file_hash


if __name__ == "__main__":
    if len(sys.argv) == 2:
        file = sys.argv[1]
        if not os.path.exists(file):
            file = os.path.join(os.path.dirname(__file__), file)
            if not os.path.exists(file):
                print("cannot found file")
            else:
                file_md5(file)
        else:
            file_md5(file)
    else:
        print("no filename")
