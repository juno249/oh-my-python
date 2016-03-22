# -*- coding: utf-8 -*-

"""
    cron_task.py
    ~~~~~~~
    * Copyright (C) 2016 GridSafe, Inc.
"""
import logging

from worker import celery_app


@celery_app.task(name="app.tasks.sample")
def sample():
    logging.info('This is a sample for flask-celery')
