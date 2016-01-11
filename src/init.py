#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @author:Hieda no Chiaki <i@wind.moe>

import platform


def p():
    global sys
    print(platform.system())
    s = platform.system()
    if s == 'Windows':
        sys = 'Windows'
    elif s == 'Darwin':
        sys = 'MacOS'
    else:
        sys = 'Linux'


def usage():
    print(1)

if __name__ == "__main__":
    p()
