#! -*- encoding:utf-8 -*-
import requests


class IProxyCrawler(object):
    """
    代理网站抓取，定义了一些公用基础操作
    """

    def __init__(self, url, headers):
        self.url = url
        self.headers = headers
        self.proxies = set()
        self.crawl_proxies = None

    def fetch_content(self, proxies=None):
        if proxies is None:
            xx = requests.get(self.url, headers=self.headers)
            return xx.text
        else:
            xx = requests.get(self.url, proxies=proxies, headers=self.headers)
            if xx.status_code == 200:
                return xx.text
            else:
                raise RuntimeError("无效的代理")

    def crawl(self):
        """
        爬取代理网站的网页
        :return:
        """
        raise NotImplementedError("Should have implemented this")

    def parse_ip_list(self, content):
        """
        解析代理网站上的ip地址数据
        :return:
        """
        raise NotImplementedError("Should have implemented this")

    def set_crawl_proxies(self, proxies):
        self.crawl_proxies = proxies

    def test(self):
        raise NotImplementedError("Should have implemented this")
