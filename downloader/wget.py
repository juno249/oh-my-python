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

    def __init__(self, filename=None, config={}):
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
        headers = {
            'Range': 'bytes=0-4'
        }
        try:
            r = requests.head(url, headers=headers)
            crange = r.headers['content-range']
            self.total = int(re.match(ur'^bytes 0-4/(\d+)$', crange).group(1))
            return True
        except:
            pass
        try:
            self.total = int(r.headers['content-length'])
        except:
            self.total = 0
        return False

    def download(self, url, filename=None, headers={}):
        finished = False
        block = self.config['block']
        if filename is None:
            filename = self.get_filename_from_url(url)

        local_filename = self.remove_nonchars(filename)
        tmp_filename = local_filename + '.downtmp'
        size = self.size
        total = self.total
        if self.support_continue(url):  # 支持断点续传
            try:
                with open(tmp_filename, 'rb') as fin:
                    self.size = int(fin.read())
                    size = self.size + 1
            except:
                self.touch(tmp_filename)
            finally:
                headers['Range'] = "bytes=%d-" % (self.size, )
        else:
            self.touch(tmp_filename)
            self.touch(local_filename)

        r = requests.get(url, stream=True, verify=False, headers=headers)
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
                        '\b' * 64 + 'now: %d, total: %s' % (size, total))
                    sys.stdout.flush()
                finished = True
                os.remove(tmp_filename)
                spend = int(time.time() - start_t)
                speed = int((size - self.size) / 1024 / spend)
                sys.stdout.write(
                    ('\nDownload finished!\nTotal time: %ss,'
                     ' Download speed: %sk/s\n') % (spend, speed))
                sys.stdout.flush()
            except Exception as err:
                track = traceback.format_exc()
                logging.error('%s\n%s', err, track)
            finally:
                if not finished:
                    with open(tmp_filename, 'wb') as ftmp:
                        ftmp.write(str(size))


if __name__ == '__main__':
    args = sys.argv
    if len(args) < 2:
        print 'python2 wget.py url'
        sys.exit(1)
    url = args[1]
    PyWget().download(url)
