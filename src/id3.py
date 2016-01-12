#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @author:Hieda no Chiaki <i@wind.moe>

import codecs
import json
import logging;logging.basicConfig(level=logging.INFO)
import os


def getID3(file):

    f = os.path.split(os.path.realpath(__file__))[0] + "\media.json"
    cmd = "cd src\win & ffprobe -v quiet -print_format json -show_format " + file + " > " + f
    os.system(cmd)
    tmpfile = codecs.open(f, 'rb', 'utf-8')
    tmp = tmpfile.read()
    tmpfile.close()
    s = json.loads(tmp)
    flag = 1
    try:
        bit_rate = int(s['format']['bit_rate'])
        format_name = s['format']['format_name']
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


if __name__ == "__main__":
    pass
