# coding: utf-8
from __future__ import absolute_import
from datetime import timedelta

from celery.schedules import crontab

BROKER_URL = 'redis://127.0.0.1:6379/2'

# 指定时区
CELERY_TIMEZONE = 'Asia/Shanghai'

# 指定是那个队列处理
CELERY_ROUTES = {
    'sample.tasks.add': {'queue': 'add-action'},
    'sample.tasks.minus': {'queue': 'minus-action'}
}

# 添加一些定时任务
CELERY_SCHEDULE = {
    'add': {
        'task': 'sample.tasks.add',
        'schedule': timedelta(seconds=10),
        'args': (16, 15)
    },
    'minus': {
        'task': 'sample.tasks.minus',
        'schedule': crontab(minute='*/3'),
        'args': (24, 13)
    },
    'remind': {
        'task': 'sample.tasks.remind',
        'schedule': crontab(hour='*/1', minute=45)
    },
}
