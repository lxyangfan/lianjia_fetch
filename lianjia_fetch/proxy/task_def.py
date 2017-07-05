#! -*- encoding:utf8 -*-

import time, csv, re, requests
from bs4 import BeautifulSoup as Bs
from lianjia_fetch.crawler.lianjia_crawler import  LianJiaSHCrawler

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,fr-FR;q=0.6,fr;q=0.4,en-US;q=0.2,en;q=0.2',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}


class BaseTask(object):
    def __init__(self):
        pass

    def run_task(self):
        return None

    def __str__(self):
        pass


class VarifyProxyTask(object):
    """ Varify proxy task """

    def __init__(self, url, timeout=0.5):
        self.url = url
        self.timeout = timeout

    def __call__(self):
        proxies = {'http': self.url, 'https': self.url}
        try:
            print 'testing proxy....'
            r = requests.get('http://icanhazip.com', proxies=proxies, timeout=self.timeout)
            if r.status_code == 200:
                print 'Got one!'
                return self.url
            else:
                return None
        except:
            return None

    def __str__(self):
        return 'VarifyProxyTask Url: %s  ' % (self.url)


class CrawTask(object):
    """ Craw proxy task"""

    def __init__(self, url):
        self.url = url
        self.proxies = set()

    def __call__(self):
        xx = requests.get(self.url, headers=headers)
        soup = Bs(xx.text, "lxml")
        ip_list = soup.find_all('tr', class_='odd')
        for item in ip_list:
            col_list = re.split(r'\s*', item.text)
            if col_list[4] == u'高匿':
                proxy = col_list[1] + ':' + col_list[2]
                self.proxies.add(proxy)
        return self

    def __str__(self):
        return 'Craw Url: %s  ' % self.url


class CrawlLianjiaTask(object):
    """ CrawlLianjiaTask  task """

    def __init__(self, url, proxy_ip=None):
        self.url = url
        if proxy_ip is None:
            self.proxy = None
        else:
            self.proxy = {'http': proxy_ip, 'https': proxy_ip}
        self.crawler = LianJiaSHCrawler(url=url, proxies=self.proxy)

    def __call__(self):
        try:
            res = self.crawler.crawl()
            return res
        except:
            return None
