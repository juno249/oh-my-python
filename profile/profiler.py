# -*- coding: utf-8 -*-
"""新能测试模块

usage:
    import profiler
    ...
    @profiler.profile
    def func(*args, **kwargs):
        ....
"""
import pstats
import tempfile
import cProfile
import functools


def profile(func):
    @functools.wraps(func)
    def __profile(*args, **kw):
        s = tempfile.mktemp()
        profiler = cProfile.Profile()
        retval = profiler.runcall(func, *args, **kw)
        profiler.dump_stats(s)
        p = pstats.Stats(s)
        p.sort_stats('time').print_stats(5)
        return retval

    return __profile


if __name__ == "__main__":

    @profile
    def factorial(n):
        result = 1
        for n in range(1, n+1):
            result *= n
        return result

    n = factorial(10)
    print n
