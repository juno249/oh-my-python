# -*- coding: utf-8 -*-
"""一个简易的缓存装饰器
usage:
    from cache import cache

    @cache
    def func(*args, **args):
        ...
"""
import time
import hashlib

info_cache = {}


def is_timeout(entry, duration):
    return time.time() - entry['time'] > duration


def compute_key(function, args, kwargs):
    key = '{}{}{}'.format(function.func_name, args, kwargs)
    return hashlib.sha1(key).hexdigest()


def cache(duration=1800):
    def _cache(function):
        def __cache(*args, **kwargs):
            key = compute_key(function, args, kwargs)
            if key in info_cache and not is_timeout(info_cache[key], duration):
                return info_cache[key]['value']

            result = function(*args, **kwargs)
            info_cache[key] = {'value': result, 'time': time.time()}
            return result
        return __cache
    return _cache
