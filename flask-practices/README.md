##some note about flask
###some suggestions
1. 为flask应用创建一个单独的虚拟环境，用virtualenv。
2. 尽可能的使用扩展实现而不是自己造轮子。

###some useful flask-plugin
1. Flask-Script
Flask-Script 是一个 Flask 扩展,为 Flask 程序添加了一个命令行解析器。Flask-Script 自带了一组常用选项,而且还支持自定义命令。
安装
```
pip install flask-script
```
使用
```python
# coding: utf-8
# hello.py
from flask.ext.script import Manager
manager = Manager(app)
# ...
if __name__ == '__main__':
manager.run()
```
2. Flask-SQLAlchemy
Flask-SQLAlchemy 是一个 Flask 扩展,简化了在 Flask 程序中使用 SQLAlchemy 的操作。SQLAlchemy 是一个很强大的关系型数据库框架,支持多种数据库后台。SQLAlchemy 提供了高层 ORM,也提供了使用数据库原生 SQL 的低层功能。
安装
```
pip install flask-sqlalchemy
```
3. Flask-Migrate
SQLAlchemy的主力开发人员编写了一个迁移框架,称为 [Alembic](https://alembic.readthedocs)。除了直接使用Alembic之 外,Flask程序还可使用[Flask-Migrate](http://flask-migrate.readthedocs.org/en/latest/)扩展。这个扩展对 Alembic 做了轻量级包装,并集成到 Flask-Script 中,所有操作都通过 Flask-Script 命令完成。
安装
```
pip install flask-migrate
```
使用
```python
from flask.ext.migrate import Migrate, MigrateCommand
# ...
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)
```
4. Flask-Email

### 大型项目结构
1. 配置选项
程序经常需要设定多个配置。这方面最好的例子就是开发、测试和生产环境要使用不同的数据库,这样才不会彼此影响。