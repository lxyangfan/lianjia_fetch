#! -*- encoding:utf-8 -*-
from proxy_crawler import IProxyCrawler

class MockIPCrawler(IProxyCrawler):
    """
      虚拟的proxy IP Crawler, 用于提供测试
    """

    def __init__(self, url, headers):
      super(MockIPCrawler, self).__init__(url, headers)

    def crawl(self):
        """
        爬取代理网站的网页
        :return:
        """
        self.proxies = set([
            '127.0.0.1:9222',
            '127.0.0.1:9223',
            '127.0.0.1:9224',
            '127.0.0.1:9225',
            '127.0.0.1:9225'
          ])
        return self.proxies

    def __str__(self):
        str = ""
        for i in list(self.proxies):
            str = "{0},{1}".format(str, i)
        return str



if __name__ == "__main__":
    print u"设定mock"
    crawler = MockIPCrawler("localhost", headers=None)
    crawler.crawl()
    print "mooc result: "
    print crawler
