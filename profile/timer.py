#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""程序片函数运行时间测量模块
usage:
    from timer import howlongitrun
    ...
    with Timer():
        ...
"""
import gc
import timeit
import functools


class Timer(object):

    def __init__(self, funcname, timer=None, disable_gc=False):
        if timer is None:
            timer = timeit.default_timer
        self.funcname = funcname
        self.timer = timer
        self.disable_gc = disable_gc
        self.start = self.end = self.interval = None

    def __enter__(self):
        if self.disable_gc:
            self.gc_state = gc.isenabled()
            gc.disable()
        self.start = self.timer()
        return self

    def __exit__(self, *args):
        self.end = self.timer()
        if self.disable_gc and self.gc_state:
            gc.enable()
        self.interval = (self.end - self.start)*1000
        s = ' '.join(['func:', self.funcname, 'takes {0} ms'.format(
                     self.interval)])
        print s


def howlongitrun(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        with Timer(func.__name__):
            retval = func(*args, **kwargs)
        return retval
    return wrapper


if __name__ == "__main__":
    @howlongitrun
    def factorial(n):
        result = 1
        for n in range(1, n+1):
            result *= n
        return result

    n = factorial(10)
    print n
