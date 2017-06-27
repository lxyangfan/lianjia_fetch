#! -*- encoding:utf-8 -*-

from lianjia_crawler import LianJiaSHCrawler
from proxy.lib.file_util import save_prop_csv
from threading import *

def task():
    crawler = LianJiaSHCrawler()
    res = crawler.crawl()
    save_prop_csv("res.csv", res, mode="w")

if __name__ == "__main__":
    print "开始抓取..."
    th1 = Thread(target=task, name="work1", args=())
    th1.start()
    th1.join()
    print "结束！！"
