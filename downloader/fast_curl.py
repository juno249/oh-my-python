# -*- coding: utf-8 -*-
"""一个基于PyCurl多线程的下载模块
"""
import os
import sys
import time
import shutil
import logging
import traceback
from threading import Thread

import pycurl
import requests


class Worker(Thread):

    def __init__(self, thread_name, url, filename, ranges, config={}):
        super(Worker, self).__init__()
        self.name = thread_name
        self.url = url
        self.filename = filename
        self.ranges = ranges
        self.downloaded = 0
        self.config = {}
        self.config.update(config)

    def progress(self, total, existing, upload_t, upload_d):
        self.downloaded = existing

    def run(self):
        start = time.time()
        try:
            self.downloaded = os.path.getsize(self.filename)
            file_buffer = open(self.filename, 'ab+')
        except OSError:
            self.downloaded = 0
            file_buffer = open(self.filename, 'wb')

        self.startpoint = self.ranges[0] + self.downloaded
        if self.startpoint >= self.ranges[1]:
            logging.info('Part %s has been downloaded over' % self.filename)
            return

        logging.info('task {} will download from {} to  {}'.format(self.name,
                     self.startpoint, self.ranges[1]))

        curl = get_base_curl(self.url)
        curl.setopt(pycurl.WRITEFUNCTION, file_buffer.write)

        # 设置Range不在头部设置
        down_range = '{}-{}'.format(int(self.startpoint), int(self.ranges[1]))
        curl.setopt(pycurl.RANGE, down_range)
        curl.setopt(pycurl.NOPROGRESS, False)
        curl.setopt(pycurl.PROGRESSFUNCTION, self.progress)
        try:
            curl.perform()
        except Exception as err:
            track = traceback.format_exc()
            msg = '%s\n%s' % (err, track)
            logging.error(msg)
            return -1
        finally:
            curl.close()
            file_buffer.close()
        interval = time.time() - start
        logging.info('thread_{} finish download Range:{}-{}, takes {}s'.format(
            self.name, self.ranges[0], self.ranges[1], interval))
        return 0


def get_base_curl(url):
    curl = pycurl.Curl()
    curl.setopt(pycurl.URL, url)
    curl.setopt(pycurl.MAXREDIRS, 5)
    curl.setopt(pycurl.FOLLOWLOCATION, True)
    curl.setopt(pycurl.TIMEOUT, 1200)
    curl.setopt(pycurl.CONNECTTIMEOUT, 1200)
    curl.setopt(pycurl.NOSIGNAL, True)
    return curl


def get_total_size(url, valid_type=None):
    """获取要下载的文件的大小及格式
    """
    r = requests.head(url, allow_redirects=True)
    total_size = int(r.headers.get('Content-Length', 0))
    ctype = r.headers.get('Content-Type', '')
    media_type = ctype.split('/')[0]
    if not media_type or media_type not in valid_type:
        total_size = 0
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


def cal_suitable_blocks(size):
    """根据下载的大小计算分成几块
    """
    size_500m = 524288000
    min_count = 5
    max_count = 10
    if size < size_500m:
        return min_count
    return max_count


def fast_curl(url, output, blocks=None, config={}):
    start_time = time.time()
    total_size = get_total_size(url, valid_type=('video',))

    if blocks is None:
        blocks = cal_suitable_blocks(total_size)
    ranges = split_blocks(total_size, blocks)

    if total_size <= 0:
        logging.info('Target url not accessible.')
        return -1

    threads = ['thread_{}'.format(n) for n in range(0, blocks)]
    files = ['{}_tmpfile_{}'.format(output, n) for n in range(0, blocks)]

    tasks = []
    for n in range(0, blocks):
        task = Worker(threads[n], url, files[n], ranges[n])
        task.daemon = True
        task.start()
        tasks.append(task)

    # 以下时进度条提示
    toolbar_width = 40
    while is_live(tasks):
        downloaded = sum([t.downloaded for t in tasks])
        interval = time.time() - start_time
        if interval and not (interval % 10.0):
            process = downloaded / float(total_size)
            text = "[{0}{1}] {2:.2f}% {3}/{4} {5:.2f}KB/s".format(
                '#'*int(process * toolbar_width),
                ' '*int((1-process) * toolbar_width),
                process * 100,
                int(downloaded), total_size,
                downloaded / 1024.0 / interval)
            logging.info(text)

    with open(output, 'wb+') as outfile:
        for n in files:
            with open(n, 'rb') as infile:
                shutil.copyfileobj(infile, outfile, 102400)
            try:
                os.remove(n)
            except OSError:
                pass

    interval = time.time() - start_time
    speed = total_size / 1024.0 / interval
    logging.info('-' * 80)
    logging.info('[Download {0} takes {1:.2f}s, speed: {2:.2f}KB/s] {3:.2f}MB'
                 .format(url, interval, speed, total_size/1048576.0))
    return 0
