# coding: utf-8
from __future__ import absolute_import
import logging
from datetime import datetime

from sample.celery import app


@app.task
def add(x, y):
    result = x+y
    with open('/tmp/add', 'w') as outfile:
        outfile.write('process result: %s' % str(result))
    return result


@app.task
def minus(x, y):
    result = x - y
    with open('/tmp/minus', 'w') as outfile:
        outfile.write('process result: %s' % str(result))
    logging.info('minus result %d', result)
    return result


@app.task
def remind():
    current = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open('/tmp/remind', 'w') as outfile:
        outfile.write('now : %s' % current)
    logging.info('now: %s', current)
