# -*- coding: utf-8 -*-
__author__ = 'yijingping'
import redis
import json
from django.conf import settings
from hashlib import md5
from django.shortcuts import redirect

REDIS_POOL = None


# def get_redis_pool():
#     global REDIS_POOL
#     if not REDIS_POOL:
#         REDIS_POOL = redis.ConnectionPool(**settings.REDIS_OPTIONS)
#
#     return REDIS_POOL


class Singleton(object):
    def __new__(cls, *args, **kw):
        # cls.kw可用与对比传入的参数：
        # 若应用中只有一套参数，就存在一个实例；若有多套参数，就应该有多个实例。
        if hasattr(cls, '_instance') and cls.kw == kw:
            pass
        else:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kw)
            cls.kw = kw
            # print cls.kw
        return cls._instance


class RedisSingle(Singleton):
    def __init__(self, redis_config):
        host, port, db, password = redis_config['host'], redis_config['port'], \
                                   redis_config['db'], redis_config['password'],
        self.client = redis.Redis(host, port, db, password)


def get_redis():
    return RedisSingle(settings.REDIS_OPTIONS).client


def get_uniqueid(url):
    link = get_link_from_url(url)
    return md5(link).hexdigest()


def get_link_from_url(url):
    if isinstance(url, basestring):
        return url
    elif isinstance(url, dict):
        return json.dumps(url)


def login_required(f):
    """
    要求登录的decorator
    :param f: 函数
    :return:
    """

    def _wrapper(request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated():
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        else:
            # request_context = RequestContext(request)
            # request_context.push({"admin_user": user})
            return f(request, *args, **kwargs)

    return _wrapper
