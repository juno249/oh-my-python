首先启动celery server
```
celery worker -A app.worker.celery_app -l info
```
运行beat，定时任务发送待队列
```
celery -A app.mgtv_worker.celery_app beat
```
