#! -*- encoding:utf-8 -*-
from threading import Thread


class ProxyProducer(Thread):
    """
    代理IP池生产者线程，向池子中加入未处理的IP
    """

    def __init__(self, event, pool, name=None):
        super(ProxyProducer, self).__init__(name=name)
        self.event = event
        # 线程安全的代理IP池
        self.pool = pool
        self.crawler = self.pool.get_crawler()

    def run(self):
        while not self.pool.full():
            # 从pool中获取一个稳定的代理，用于爬取免费代理网站
            stable_proxies = self.pool.get_stable_proxies()
            if stable_proxies is not None:
                self.crawler.set_proxies(stable_proxies)

            proxies = list(self.crawler.crawl())
            if len(proxies):
                for proxy in proxies:
                    self.pool.add(proxy)
