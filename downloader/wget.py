# -*- coding: utf-8 -*-
"""一个基于requests的断点下载模块
usage:
    from wget import PyWget

    downloader = PyWget(filename)
    downloader.download(url)
"""
import os
import re
import sys
import time
import logging
import traceback
from urlparse import urlparse

import requests


class PyWget(object):

    def __init__(self, config={}):
        self.config = {
            'block': config.get('block') if 'block' in config else 10240,
        }
        self.total = 0
        self.size = 0
        self.filename = ''

    def touch(self, filename):
        if not os.path.exists(filename):
            os.mknod(filename)

    def get_filename_from_url(self, url):
        url_path = urlparse(url).path
        return os.path.basename(url_path)

    def remove_nonchars(self, name):
        (name, _) = re.subn(ur'[\\\/\:\*\?\"\<\>\|]', '', name)
        return name

    def support_continue(self, url):
        r = requests.head(url, allow_redirects=True)
        crange = r.headers.get('content-range')
        if crange:
            self.total = int(re.match(ur'^bytes 0-4/(\d+)$', crange).group(1))
            return True

        self.total = int(r.headers.get('Content-Length', 0))
        return False

    def download(self, url, filename=None, headers={}):
        finished = False
        block = self.config['block']
        if filename is None:
            filename = self.get_filename_from_url(url)

        local_filename = self.remove_nonchars(filename)
        tmp_filename = local_filename + '.downtmp'
        size = self.size

        # 支持断点下载
        if self.support_continue(url):
            try:
                with open(tmp_filename, 'rb') as fin:
                    self.size = int(fin.read())
                    size = self.size + 1
            except:
                self.touch(tmp_filename)
            finally:
                headers['Range'] = "bytes=%d-" % self.size
        else:
            self.touch(tmp_filename)
            self.touch(local_filename)

        total = self.total

        r = requests.get(url, stream=True, headers=headers)
        if total > 0:
            logging.info("[+] Size: %dKB", (total / 1024))
        else:
            logging.info("[+] Size: None")
        start_t = time.time()
        with open(local_filename, 'ab+') as f:
            f.seek(self.size)
            f.truncate()
            try:
                for chunk in r.iter_content(chunk_size=block):
                    if chunk:
                        f.write(chunk)
                        size += len(chunk)
                        f.flush()
                    logging.info(
                        'now: {0:.2f}KB, total: {1:.2f}kB, {2:.2f}%'.format(
                            size / 1024.0, total / 1024.0, size * 100.0 / total
                        ))
                    sys.stdout.flush()
                finished = True
                os.remove(tmp_filename)
                spend = int(time.time() - start_t)
                speed = int((size - self.size) / 1024 / spend)
                sys.stdout.write(
                    ('\nDownload finished!\nTotal time: %ss,'
                     ' Download speed: %sKB/s\n') % (spend, speed))
                sys.stdout.flush()
            except Exception as err:
                track = traceback.format_exc()
                logging.error('%s\n%s', err, track)
            finally:
                if not finished:
                    with open(tmp_filename, 'wb') as ftmp:
                        ftmp.write(str(size))


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format="%(asctime)s %(levelname)s# %(message)s",
                        datefmt="%Y/%m/%d-%H:%M:%S")
    args = sys.argv
    if len(args) < 2:
        print 'python2 wget.py filename url'
        sys.exit(1)
    filename = args[1]
    url = args[2]
    wget = PyWget()
    wget.download(url, filename)
