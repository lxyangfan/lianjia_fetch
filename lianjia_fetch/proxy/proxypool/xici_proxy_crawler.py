#! -*- encoding:utf-8 -*-
import re
from bs4 import BeautifulSoup as Bs
from proxy_crawler import IProxyCrawler


class XiciProxyCrawler(IProxyCrawler):
    """
    Xici 免费代理网站爬取
    """
    def __init__(self, url, headers):
        IProxyCrawler.__init__(self, url=url, headers=headers)

    def crawl(self):
        content = IProxyCrawler.fetch_content(self)
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
