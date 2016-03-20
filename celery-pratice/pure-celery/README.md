### celery
celery是一个优秀的任务的分布式任务调度系统，可以取代crontab来做一些任务调度。

调用命令:
```
celery worker --app=sample -l info
```
然后：
```
celery -A sample beat
```
这个命令会定时将任务发送到celery的任务队列
