#! -*- encoding:utf-8 -*-
import re, requests, random



class IProxyCrawler(object):
    """
    代理网站抓取，定义了一些公用基础操作
    """

    def __init__(self, url, headers):
        self.url = url
        self.headers = headers
        self.proxies = set()

    def fetch_content(self):
        xx = requests.get(self.url, headers=self.headers)
        return xx.text

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

    def test(self):
        raise NotImplementedError("Should have implemented this")
