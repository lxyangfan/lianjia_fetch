#! -*- encoding:utf-8 -*-
import re
import logging
from bs4 import BeautifulSoup as Bs
from proxy_crawler import IProxyCrawler
from thread_safe_set import LockedSet
from multiprocessing import Lock

logger2 = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger2.addHandler(handler)
logger2.setLevel(logging.DEBUG)

class XiciProxyCrawler(IProxyCrawler):
    """
    Xici 免费代理网站爬取
    """
    visit_pages = LockedSet()
    base_url = "http://www.xicidaili.com/nn/"

    def __init__(self, headers):
        super(XiciProxyCrawler, self).__init__(url=XiciProxyCrawler.base_url+'1', headers=headers)
        self.next_page = 1
        self.lock = Lock()

    def has_visit(self):
        return self.url in XiciProxyCrawler.visit_pages

    def fetch_content(self):
        if not self.url in XiciProxyCrawler.visit_pages:
            # 添加本URL到集合
            XiciProxyCrawler.visit_pages.add(self.url)
            return super(XiciProxyCrawler, self).fetch_content()

    def crawl(self):
        if self.has_visit():
            self.get_next_url()
            logger2.debug("Cur url - {}".format(self.url))

        content = self.fetch_content()
        self.parse_ip_list(content)
        return self.proxies

    def parse_ip_list(self, content):
        soup = Bs(content, "lxml")
        ip_list = soup.find_all('tr', class_='odd')
        for item in ip_list:
            col_list = re.split(r'\s*', item.text)
            if col_list[4] == u'高匿':
                proxy = col_list[1] + ':' + col_list[2]
                self.proxies.add(proxy)
        return self.proxies

    def get_next_url(self):
        with self.lock:
            self.next_page += 1
            self.url = "{0}{1}".format(XiciProxyCrawler.base_url, self.next_page)
            return self.url