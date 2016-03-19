# coding: utf-8
import time


def follow(infile):
    infile.seek(0, 2)
    while True:
        line = infile.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line
