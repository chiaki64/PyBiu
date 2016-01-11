#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @author:Hieda no Chiaki <i@wind.moe>

import sys
import os
import binascii
import json
import codecs


def getID3(file):

    f = os.path.split(os.path.realpath(__file__))[0] + "\media.json"
    cmd = "cd src\win & ffprobe -v quiet -print_format json -show_format " + file + " > " + f
    os.system(cmd)
    # "D:\Python\\WorkSpace\\Biu.moe_Uploader\\test\\This.mp3"

    # with open(f, 'rb') as string:
    #     tmp = string.decode('gbk').encode('utf-8')
    tmpfile = codecs.open(f, 'rb', 'utf-8')
    tmp = tmpfile.read()
    tmpfile.close()

    # tmp = os.popen(cmd).read()

    # print(tmp)
    s = json.loads(tmp)
    # print(s['format']['tags'])
    flag = 1
    try:
        bit_rate = int(s['format']['bit_rate'])
        format_name = s['format']['format_name']
        # print("Bit Rate: %d" % bit_rate)
        # print("Format Name: " + format_name)
        if format_name == "mp3" and bit_rate / 1000 < 300:
            return "", "", "", 0
        elif format_name == "aac" and bit_rate / 1000 < 200:
            return "", "", "", 0
        elif format_name in ["flac", "ape", "wav", "tta", "tak", "alac"]:
            pass
    except KeyError:
        return "", "", "", 0

    try:
        title = s['format']['tags']['title']
    except KeyError:
        try:
            title = s['format']['tags']['TITLE']
        except KeyError:
            return "", "", "", 2

    try:
        artist = s['format']['tags']['artist']
    except KeyError:
        try:
            artist = s['format']['tags']['ARTIST']
        except KeyError:
            artist = ""

    try:
        album = s['format']['tags']['album']
    except KeyError:
        try:
            album = s['format']['tags']['ALBUM']
        except KeyError:
            album = ""

    return title, artist, album, flag


# ffprobe -v quiet -print_format json -show_format D:\Python\WorkSpace\Biu.moe_Uploader\test\dream.mp3 @echo off

# flag 0 码率不对 1 允许上传 2 title不完整

if __name__ == "__main__":
    getID3("1")
    # if len(sys.argv) == 2:
    #     file = sys.argv[1]
    #     if not os.path.exists(file):
    #         file = os.path.join(os.path.dirname(__file__), file)
    #         if not os.path.exists(file):
    #             print("cannot found file")
    #         else:
    #             getID3(file)
    #     else:
    #         getID3(file)
    # else:
    #     print("no filename")
