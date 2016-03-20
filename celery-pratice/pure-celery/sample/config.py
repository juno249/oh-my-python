# coding: utf-8
from __future__ import absolute_import

from celery.schedules import crontab
from kombu import Exchange, Queue

BROKER_URL = 'redis://127.0.0.1:6379/2'

# 指定时区
CELERY_TIMEZONE = 'Asia/Shanghai'

CELERY_QUEUES = (
    Queue('default', Exchange('default'), routing_key='default'),
    Queue('for_add_task', Exchange('for_add_task'), routing_key='add_task'),
    Queue('for_minus_task', Exchange('for_minus_task'),
          routing_key='minus_task'),
)

# 指定是那个队列处理
CELERY_ROUTES = {
    'sample.tasks.add': {'queue': 'for_add_task', 'routing_key': 'add_task'},
    'sample.tasks.minus': {'queue': 'for_task_minus',
                           'routing_key': 'minus_task'},
    'sample.tasks.remind': {'queue': 'default', 'routing_key': 'default'}

}

# 添加一些定时任务
CELERYBEAT_SCHEDULE = {
    'add': {
        'task': 'sample.tasks.add',
        'schedule': 10,
        'args': (16, 15),
    },
    'minus': {
        'task': 'sample.tasks.minus',
        'schedule': 30,
        'args': (24, 13),
    },
    'remind': {
        'task': 'sample.tasks.remind',
        # crontab 的最小粒度是minute
        'schedule': crontab(minute='*/1'),
    },
}
