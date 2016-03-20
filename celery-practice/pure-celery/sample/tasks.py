# coding: utf-8
from __future__ import absolute_import
import logging
from datetime import datetime

from sample.celery import app


@app.task(name='sample.tasks.add')
def add(x, y):
    result = x+y
    logging.info('add result %s', str(result))
    return result


@app.task(name='sample.tasks.minus')
def minus(x, y):
    result = x - y
    logging.info('minus result %s', str(result))
    return result


@app.task(name='sample.tasks.remind')
def remind():
    current = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logging.info('now: %s', current)
