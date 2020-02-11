# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from twisted.internet import defer
from twisted.internet.error import TimeoutError, DNSLookupError, \
        ConnectionRefusedError, ConnectionDone, ConnectError, \
        ConnectionLost, TCPTimedOutError
from twisted.web.client import ResponseFailed
from pymongo.errors import DuplicateKeyError
from scrapy.core.downloader.handlers.http11 import TunnelError


import redis
import random
import re

class Proxy_Middleware(object):


    '''随机IP'''
    EXCEPTIONS_TO_RETRY = (defer.TimeoutError, TimeoutError, DNSLookupError,
                           ConnectionRefusedError, ConnectionDone, ConnectError,
                           ConnectionLost, TCPTimedOutError, ResponseFailed,
                           IOError, TunnelError, DuplicateKeyError)

    def process_request(self, request, spider):
        self.reids_pool = redis.Redis(host='127.0.0.1', port=6379)
        proxies = self.reids_pool.hgetall('proxies')
        keys = []
        for key in proxies.keys():
            keys.append(key.decode('utf-8'))
        proxy = random.choice(keys)
        request.meta['proxy'] = 'http://' + proxy
        return None

    def process_exception(self, request, exception, spider):
        if isinstance(exception, self.EXCEPTIONS_TO_RETRY):
            ip = re.findall('http://(.*?:\d+)', request.meta['proxy'])[0]
            print(ip)
            self.reids_pool.hdel('proxies', ip)
            proxies = self.reids_pool.hgetall('proxies')
            keys = []
            for key in proxies.keys():
                keys.append(key.decode('utf-8'))
            proxy = random.choice(keys)
            print('更换ip' + proxy)
            request.meta['proxy'] = "http://" + proxy

    def process_response(self,request,response,spider):
        #如果该ip不能使用，更换下一个ip
        if response.status != 200:
            ip = re.findall('http://(.*?:\d+)', request.meta['proxy'])[0]
            self.reids_pool.hdel('proxies', ip)
            proxies = self.reids_pool.hgetall('proxies')
            keys = []
            for key in proxies.keys():
                keys.append(key.decode('utf-8'))
            proxy = random.choice(keys)
            print('更换ip'+proxy)
            request.meta['proxy'] = "http://" + proxy
            return request
        return response

