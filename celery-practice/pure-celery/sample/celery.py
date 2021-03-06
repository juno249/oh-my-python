# coding: utf-8
from __future__ import absolute_import
from celery import Celery

app = Celery('sample',
             include=['sample.tasks'])

app.config_from_object('sample.config')

app.conf.update(CELERY_TASK_RESULT_EXPIRES=3600,)


if __name__ == "__main__":
    app.run()
