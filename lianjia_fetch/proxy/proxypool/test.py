#! -*- encoding:utf-8 -*-
from xici_proxy_crawler import XiciProxyCrawler
from threading import Thread
from multiprocessing import Queue
from logging.config import fileConfig
import time
import logging

fileConfig("log-conf.ini")
logger = logging.getLogger("debugLog")

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,fr-FR;q=0.6,fr;q=0.4,en-US;q=0.2,en;q=0.2',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

queue = Queue()

def task():
    v = XiciProxyCrawler(headers=headers)
    res = list(v.crawl())
    if len(res):
        for i in res:
            queue.put(i)
        time.sleep(1)
    else:
        logger.warn("没有结果！")


if __name__ == "__main__":
    th1 = Thread(target=task, name="work1")
    th2 = Thread(target=task, name="work2")

    th1.start()
    th2.start()

    logger.debug("开启2个线程抓取...")

    th1.join()
    th2.join()
    logger.debug("2个线程抓取结束...")

    while not queue.empty():
        item = queue.get()
        logger.info("item-{}".format(item))
