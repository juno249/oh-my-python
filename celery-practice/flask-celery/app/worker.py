# -*- coding: utf-8 -*-

"""
    worker.py
    ~~~~~~~
    * Copyright (C) 2016 GridSafe, Inc.
"""
from __future__ import absolute_import

from celery import Celery
from flask import Flask

from app.models import db

app = Flask(__name__)
app.config.update(
    SQLALCHEMY_DATABASE_URI='mysql://root:@localhost/database_name',
    SQLALCHEMY_TRACK_MODIFICATIONS=True,
)
db.init_app(app)


def make_celery(app):
    celery = Celery(app.import_name,
                    include=['app.tasks'])

    celery.config_from_object('app.config')
    celery.conf.update(app.config)

    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


celery_app = make_celery(app)
