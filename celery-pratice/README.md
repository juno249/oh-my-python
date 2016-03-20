### some note about Celery
#### basic
##### install celery
```
sudo pip install celery
```
##### choose broker
* RabbitMQ
```
sudo apt-get install rabbitmq-server
```
* Redis
* SQLAlchemy||Django Database (not reconmended)

##### ceate application
```python
# -*- coding: utf-8
# task.py
from celery import Celery
app = Celery('tasks', broker='amqp://guest@localhost//')
@app.task
def add(x, y):
	return x + y
```
then run it:
```
celery -A tasks worker --loglevel=info
```
##### calling the task
```python
>>> from tasks import add
>>> add.delay(4,4)
```
#### keeping results 
If you want to keep track of the tasks’ states, Celery needs to store or send the states somewhere. There are several built-in result backends to choose from: SQLAlchemy/Django ORM, Memcached, Redis, AMQP (RabbitMQ), and MongoDB – or you can define your own.
```python
app = Celery('tasks', backend='redis://localhost', broker='amqp://')
```