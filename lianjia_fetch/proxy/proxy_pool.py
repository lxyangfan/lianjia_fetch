#!/bin/bash/python
# ! -*- encoding:utf8 -*-

__author__ = "frank.yang"
__date__ = "2017.6.18"

import re, requests, random
from bs4 import BeautifulSoup as Bs

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,fr-FR;q=0.6,fr;q=0.4,en-US;q=0.2,en;q=0.2',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}


class GatherProxy(object):
    '''To get proxy from http://www.xicidaili.com/nn/'''
    url = 'http://www.xicidaili.com/nn/'
    proxies = set()

    def fetch_proxies(self, pages=1):
        xx = requests.get(self.url, headers=headers)
        soup = Bs(xx.text, "lxml")
        ip_list = soup.find_all('tr', class_='odd')
        for item in ip_list:
            col_list = re.split(r'\s*', item.text)
            if col_list[4] == u'高匿':
                proxy = col_list[1] + ':' + col_list[2]
                self.proxies.add(proxy)
        return self.proxies


    def getelite(self, pages=1):
        for i in range(1, pages + 1):
            self.fetch_proxies(i)
        return self.proxies

    def varifyproxy(self):
        for proxy in self.proxies:
            if False == self.testproxy(proxy):
                self.proxies.remove(proxy)

    def testproxy(self, proxy):
        proxies = {'http': proxy, 'https': proxy}
        try:
            print 'testing proxy....'
            r = requests.get('http://dx.doi.org', proxies=proxies, timeout=0.5)
            if (r.status_code == 200):
                print 'Got one!'
                return True
            else:
                return False
        except:
            return False


class ProxyPool(object):
    '''A proxypool class to obtain proxy'''

    gatherproxy = GatherProxy()

    def __init__(self):
        self.pool = set()

    def updateGatherProxy(self, pages=1):
        '''Use GatherProxy to update proxy pool'''
        self.pool.update(self.gatherproxy.getelite(pages=pages))

    def removeproxy(self, proxy):
        '''Remove a proxy from pool'''
        if (proxy in self.pool):
            self.pool.remove(proxy)

    def randomchoose(self, pages=1):
        '''Random Get a proxy from pool'''
        if (self.pool):
            return random.sample(self.pool, 1)[0] # it's a one item list
        else:
            self.updateGatherProxy(pages)
            return random.sample(self.pool, 1)[0] # it's a one item list

    def getproxy(self, pages=1):
        '''Get a dict format proxy randomly'''
        proxy = self.randomchoose(pages)
        proxies = {'http': proxy, 'https': proxy}
        # r=requests.get('http://icanhazip.com',proxies=proxies,timeout=1)
        try:
            print 'testing proxy....'
            r = requests.get('http://dx.doi.org', proxies=proxies, timeout=0.5)
            if (r.status_code == 200):
                print 'Got one!'
                return proxies
            else:
                self.removeproxy(proxy)
                print 'removing a useless proxy...'
                return self.getproxy(pages)
        except:
            self.removeproxy(proxy)
            return self.getproxy(pages)



if __name__ == '__main__':
    pool = ProxyPool()
    xx = pool.getproxy(5)
    print xx