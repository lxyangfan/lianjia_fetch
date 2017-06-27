#! -*- encoding:utf-8 -*-
from proxy_crawler import IProxyCrawler

class MockIPCrawler(IProxyCrawler):
    """
      虚拟的proxy IP Crawler, 用于提供测试
    """

    def __init__(self, name=None):

    def crawl(self):
        """
        爬取代理网站的网页
        :return:
        """
        return set([
            '127.0.0.1:9222',
            '127.0.0.1:9223',
            '127.0.0.1:9224',
            '127.0.0.1:9225',
            '127.0.0.1:9225'
          ])

