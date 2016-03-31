# -*- coding: utf-8 -*-
"""一个基于requests多线程的下载模块
usage:
    from wget import PyWget

    downloader = PyWget()
    downloader.download(url, filename)
"""
import os
import sys
import time
import shutil
import logging
import traceback
from threading import Thread

import requests


class Worker(Thread):

    def __init__(self, thread_name, url, filename, ranges, config={}):
        super(Worker, self).__init__()
        self.name = thread_name
        self.url = url
        self.filename = filename
        self.ranges = ranges
        self.downloaded = 0
        if 'block' not in config:
            self.config = {'block': 32768}
        self.config.update(config)

    def run(self):
        try:
            self.downloaded = os.path.getsize(self.filename)
        except OSError:
            self.downloaded = 0

        self.startpoint = self.ranges[0] + self.downloaded
        if self.startpoint >= self.ranges[1]:
            logging.info('Part %s has been downloaded over' % self.filename)
            return

        block = self.config.get('block')
        logging.info('task {} will download from {} to  {}'.format(self.name,
                     self.startpoint, self.ranges[1]))

        headers = {}
        headers['Range'] = "bytes={}-{}".format(self.startpoint,
                                                self.ranges[1])
        r = requests.get(url, stream=True, headers=headers)

        with open(self.filename, 'ab+') as infile:
            infile.seek(self.downloaded)
            infile.truncate()
            try:
                for chunk in r.iter_content(chunk_size=block):
                    if chunk:
                        infile.write(chunk)
                        self.downloaded += block
                        infile.flush()
            except Exception as err:
                track = traceback.format_exc()
                msg = '%s\n%s' % (err, track)
                logging.error(msg)

        logging.info('Thread_{0} finish download Range:{1:.2f}-{2:2.f}'.format(
            self.name, self.ranges[0], self.ranges[1]))


def get_total_size(url):
    r = requests.head(url, allow_redirects=True)
    total_size = int(r.headers.get('Content-Length', 0))
    return total_size


def split_blocks(total_size, block_count):
    block_size = total_size / block_count
    ranges = []
    for n in range(0, block_count-1):
        ranges.append((n * block_size, n * block_size + block_size - 1))
    ranges.append((block_size * (block_count - 1), total_size - 1))
    return ranges


def is_live(tasks):
    for task in tasks:
        if task.is_alive():
            return True
    return False


def pyaxel(url, output, blocks=5, config={}):

    start_time = time.time()
    total_size = get_total_size(url)
    ranges = split_blocks(total_size, blocks)

    threads = ['thread_{}'.format(n) for n in range(0, blocks)]
    files = ['{}_tmpfile_{}'.format(output, n) for n in range(0, blocks)]

    tasks = []
    for n in range(0, blocks):
        task = Worker(threads[n], url, files[n], ranges[n])
        task.daemon = True
        task.start()
        tasks.append(task)

    while is_live(tasks):
        downloaded = sum([t.downloaded for t in tasks])
        process = downloaded / float(total_size) * 100
        msg = ("total: {0:.2f}KB, downloaded: {1:.2f}KB, completed: {2:.2f}%"
               .format(total_size/1024.0, downloaded/1024.0, process))
        logging.info(msg)

    with open(output, 'wb+') as outfile:
        for n in files:
            with open(n, 'rb') as infile:
                shutil.copyfileobj(infile, outfile, 102400)
            try:
                os.remove(n)
            except OSError:
                pass

    interval = time.time() - start_time
    logging.info('Download {} takes {}s.'.format(url, interval))


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format="%(asctime)s %(levelname)s# %(message)s",
                        datefmt="%Y/%m/%d-%H:%M:%S")
    args = sys.argv
    if len(args) < 2:
        print 'python2 pyaxel.py filename url'
        sys.exit(1)
    filename = args[1]
    url = args[2]
    pyaxel(url, filename)
