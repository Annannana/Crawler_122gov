# -*- coding: utf-8 -*-
import time
import base64
import random
import hashlib


class RandomUserAgentMiddleware(object):
    def __init__(self, user_agent):
        self.user_agent = user_agent

    @classmethod
    def from_crawler(cls, crawler):
        return cls(user_agent=crawler.settings.get('PC_USER_AGENT'))

    def process_request(self, request, spider):
        ua = random.choice(self.user_agent)
        request.headers["User-Agent"] = ua


class RandomProxyMiddleware(object):
    def __init__(self, proxies):
        self.proxies = proxies

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(proxies=settings.get('PROXIES'))

    def process_request(self, request, spider):
        request.meta['proxy'] = self.proxies

class MaYiProxyMiddleware(object):
    def generate_sign(self):
        app_key = "114336114"
        app_secret = "a5ff9ee15b68003d28f17d9aa0fb0ae8"
        t = time.strftime("%Y-%m-%d %H:%M:%S")
        codes = app_secret + 'app_key' + app_key + 'timestamp' + t + app_secret
        sign = hashlib.md5(codes.encode('utf-8')).hexdigest().upper()
        auth_header = 'MYH-AUTH-MD5 app_key=' + app_key + '&timestamp=' + t + '&sign=' + sign
        return auth_header

    def process_request(self, request, spider):
        proxy_url = 'http://s5.proxy.mayidaili.com:8123'
        request.headers['Mayi-Authorization'] = self.generate_sign()
        request.meta['proxy'] = proxy_url
        if '61.166.150.125:17777' in request.url:
            url = request.url.replace('http://61.166.150.125:17777/?url=', '')
            request = request.replace(url=url, dont_filter=True)
            return request