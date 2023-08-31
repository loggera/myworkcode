# -*- coding:utf-8 -*-
from redis import StrictRedis, ConnectionPool
import loguru

lg = loguru.logger
next_r_pool = ConnectionPool(host='45.63.90.101', password='', port=8001, db=0)
next_redis_svr = StrictRedis(connection_pool=next_r_pool)


def next_get_value(cache_key):
    if next_redis_svr.get(cache_key) is not None:
        return next_redis_svr.get(cache_key).decode('utf-8')
    else:
        return None


def next_set_value(cache_key, cache_val, expires_seconds):
    next_redis_svr.set(cache_key, str(cache_val), expires_seconds)


def next_get_exists(cache_key):
    return next_redis_svr.exists(cache_key)


def next_cache_delete(cache_key):
    next_redis_svr.delete(cache_key)


# print(next_get_value('name'))