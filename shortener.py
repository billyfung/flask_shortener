import redis
import md5
import math
import os
import config
import string
from math import floor

class url_shortener:   
    def __init__(self):
        self.redis = redis.Redis(config['redis_host'], config['redis_port'])

    def shorten(self, url):
        short_id = self.redis.get('reverse-url:' + url)
        if short_id is not None:
            return short_id
        url_num = self.redis.incr('last-url-id')
        short_id = b62_encode(url_num)
        self.redis.set('url-target:' + short_id, url)
        self.redis.set('reverse-url:' + url, short_id)
        return short_id

    def b62_encode(number):
        base = string.digits + string.lowercase + string.uppercase
        assert number >= 0, 'positive integer required'
        if number == 0:
            return '0'
        base62 = []
        while number != 0:
            number, i = divmod(number, 62)
            base62.append(base[i])
        return ''.join(reversed(base62))


