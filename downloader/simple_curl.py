# -*- coding: utf-8 -*-
"""基于PyCurl的断点下载程序
"""
import os
import sys
import time
import logging
import traceback

import pycurl


def get_base_curl(url):
    curl = pycurl.Curl()
    curl.setopt(pycurl.URL, url)
    curl.setopt(pycurl.FOLLOWLOCATION, True)
    curl.setopt(pycurl.MAXREDIRS, 5)
    curl.setopt(pycurl.TIMEOUT, 600)
    curl.setopt(pycurl.CONNECTTIMEOUT, 600)
    curl.setopt(pycurl.NOSIGNAL, True)
    return curl


def progress(total2download, total_downloaded, total2upload, total_uploaded):
    if total2download and total_downloaded:
        percent = float(total_downloaded) / total2download
        rate = round(percent * 100, ndigits=2)
        logging.info('total: {0:.2f} downloaded: {1:.2f} completed:{2:.2f}%'.
                     format(total2download, total_downloaded, rate))


def simple_curl(url, output):
    start = time.time()
    curl = get_base_curl(url)
    if os.path.exists(output):
        outfile = open(output, "ab+")
        downloaded = os.path.getsize(output)
        print downloaded
    else:
        outfile = open(output, "wb")
        downloaded = 0
    if downloaded:
        curl.setopt(pycurl.RANGE, '%d-' % int(downloaded))
    curl.setopt(pycurl.VERBOSE, True)
    curl.setopt(pycurl.WRITEFUNCTION, outfile.write)
    curl.setopt(pycurl.NOPROGRESS, False)
    curl.setopt(pycurl.PROGRESSFUNCTION, progress)
    try:
        curl.perform()
    except Exception as err:
        track = traceback.format_exc()
        msg = '%s\n%s' % (err, track)
        logging.error(msg)
    finally:
        curl.close()
        outfile.close()

    spend = time.time() - start
    speed = os.path.getsize(output) / 1024.0 / spend
    logging.info('download {} takes {}s, speed {}KB/s'.format(
        url, spend, speed))


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format="%(asctime)s %(levelname)s# %(message)s",
                        datefmt="%Y/%m/%d-%H:%M:%S")
    args = sys.argv
    if len(args) < 2:
        print 'python2 simple_curl.py filename url'
        sys.exit(1)
    filename = args[1]
    url = args[2]
    simple_curl(url, filename)
