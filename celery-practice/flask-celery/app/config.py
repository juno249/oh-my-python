# coding: utf-8
from __future__ import absolute_import

BROKER_URL = 'redis://127.0.0.1:6379/2'

CELERY_TIMEZONE = 'Asia/Shanghai'

CELERYBEAT_SCHEDULE = {
    'flask-celery-sample': {
        'task': 'app.tasks.sample',
        'schedule': 10,
    }
}
