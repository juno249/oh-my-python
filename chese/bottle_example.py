# coding: utf-8
from bottle import route, run

from chese import chese


@route('/')
def index():
    chese()
    return 'hello world'


if __name__ == "__main__":
    run(host='localhost', port='8080', debug=True)
