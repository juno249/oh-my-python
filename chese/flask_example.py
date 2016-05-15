# coding: utf-8
from flask import Flask

from chese import chese

app = Flask(__name__)


@app.route('/')
def index():
    chese()
    return 'hello world'


if __name__ == "__main__":
    app.run()
