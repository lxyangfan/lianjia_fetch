#! -*- encoding:utf-8 -*-

import logging
from Queue import Queue
from thread_safe_set import LockedSet


class ProxyPool(object):
    """
    代理IP池
    """

    def __init__(self, crawler_cls):
        self.unverify_queue = Queue()
        self.unstable_set = LockedSet()
        self.stable_set = LockedSet()
        self.black_set = LockedSet()
        self.proxy_crawler = crawler_cls

    def initilize(self):
        pass





