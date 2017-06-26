#! -*- encoding:utf-8 -*-

import logging
from Queue import Queue
from thread_safe_set import LockedSet
from threading import Lock


class ProxyPool(object):
    """
    代理IP池
    """

    def __init__(self, crawler, maxSize=-1):
        self.maxSize = maxSize
        self.unverify_queue = Queue(self.maxSize)
        self.unstable_set = LockedSet()
        self.stable_set = LockedSet()
        self.black_set = LockedSet()
        self.proxy_crawler = crawler
        self.curSize = 0
        self.lock = Lock()

    def get_stable_proxies(self):
        proxy = self.stable_set.pop()
        if proxy is not None:
            self.stable_set.add(proxy)
            return {'http': proxy.url, 'https': proxy.url}
        else:
            return None

    def full(self):
        """
        判断待处理的IP池(unverify_queue) 是否已经满了
        :return:
        """
        if self.maxSize == -1:
            return False
        with self.lock:
            if self.curSize >= self.maxSize:
                return True
            else:
                return False

    def get_crawler(self):
        return self.proxy_crawler
