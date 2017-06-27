#! -*- encoding:utf-8 -*-
import requests


default_headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,fr-FR;q=0.6,fr;q=0.4,en-US;q=0.2,en;q=0.2',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

class BaseCrawler(object):
    """
    房产网站抓取，定义了一些公用基础操作
    """

    def __init__(self, url, headers=None, proxies=None):
        if headers is None:
            self.headers = default_headers
        else:
            self.headers = headers
        self.url = url
        self.proxies = proxies

    def fetch_content(self, proxies=None):
        print "fetch url: ", self.url
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

    def set_proxies(self, proxies):
        self.proxies = proxies

    def test(self):
        raise NotImplementedError("Should have implemented this")
